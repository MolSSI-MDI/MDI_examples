#include <iostream>
#include <stdio.h>
#include <time.h>
#include <string.h>
#include <mpi.h>
#include "../lib/mdi_build/molssi_driver_interface/mdi.h"

using namespace std;

int main(int argc, char **argv) {
  clock_t start, end;
  double cpu_time;
  int niterations = 100;
  MPI_Comm world_comm;
  int i;

  int natoms;         // number of atoms in the system
  double mm_energy;   // energy from the MM code
  double qm_energy;   // energy from the QM code

  // Initialize the MPI environment
  MPI_Init(&argc, &argv);

  // Ensure the mdi argument has been provided
  int iarg = 1;
  if ( !( argc-iarg >= 2 && strcmp(argv[iarg],"-mdi") == 0) ) {
    perror("The -mdi argument was not provided");
    return -1;
  }

  // Initialize the MDI driver
  world_comm = MPI_COMM_WORLD;
  int ret = MDI_Init(argv[iarg+1], &world_comm);

  // Accept a communicator from the production code
  int mm_comm = MDI_Accept_Communicator();

  start = clock();

  // Receive the number of atoms from the MM code
  MDI_Send_Command("<NATOMS", mm_comm);
  MDI_Recv(&natoms, 1, MDI_INT, mm_comm);

  // Allocate the arrays for the coordinates and forces
  double coords[3*natoms];
  double forces[3*natoms];

  // Have the MD code initialize a new MD simulation
  MDI_Send_Command("MD_INIT", mm_comm);

  // Perform each iteration of the simulation
  for (int iiteration = 0; iiteration < niterations; iiteration++) {

    // Receive the coordinates from the MM code
    MDI_Send_Command("<COORDS", mm_comm);
    MDI_Recv(&coords, 3*natoms, MDI_DOUBLE, mm_comm);

    // Send the coordinates to the QM code
    MDI_Send_Command(">COORDS", mm_comm);
    MDI_Send(&coords, 3*natoms, MDI_DOUBLE, mm_comm);

    // Have the QM code perform an SCF calculation
    //MDI_Send_Command("SCF", mm_comm);

    // Get the QM energy
    MDI_Send_Command("<ENERGY", mm_comm);
    MDI_Recv(&qm_energy, 1, MDI_DOUBLE, mm_comm);

    // Get the MM energy
    MDI_Send_Command("<ENERGY", mm_comm);
    MDI_Recv(&mm_energy, 1, MDI_DOUBLE, mm_comm);

    // Receive the forces from the QM code
    MDI_Send_Command("<FORCES", mm_comm);
    MDI_Recv(&forces, 3*natoms, MDI_DOUBLE, mm_comm);

    // Send the forces to the MM code
    MDI_Send_Command(">FORCES", mm_comm);
    MDI_Send(&forces, 3*natoms, MDI_DOUBLE, mm_comm);

    // Do an MD timestep
    MDI_Send_Command("TIMESTEP", mm_comm);

    cout << "timestep: " << iiteration << " " << mm_energy << endl;
  }

  end = clock();
  cpu_time = ((double) (end - start)) / CLOCKS_PER_SEC;

  cout << "Total time: " << cpu_time << endl;

  MDI_Send_Command("EXIT", mm_comm);

  MPI_Barrier(world_comm);

  return 0;
}
