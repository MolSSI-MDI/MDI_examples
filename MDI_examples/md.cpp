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
  int mpi_ptr;
  int mpi_rank;
  MPI_Comm world_comm;
  int i;
  double energy;

  // Initialize the MPI environment
  MPI_Init(&argc, &argv);

  // Ensure the mdi argument has been provided
  int iarg = 1;
  if ( !( argc-iarg >= 2 && strcmp(argv[iarg],"-mdi") == 0) ) {
    perror("The -mdi argument was not provided");
    return -1;
  }

  // Get the Angstrom-Bohr conversion factor
  double conversion_factor = MDI_Conversion_Factor("Angstrom","Bohr");
  printf("Conversion factor: %f\n",conversion_factor);

  // Initialize the MDI driver
  world_comm = MPI_COMM_WORLD;
  int ret = MDI_Init(argv[iarg+1], &world_comm);

  // Accept a communicator from the production code
  int mm_comm = MDI_Accept_Communicator();

  // Note: For reasons I don't fully understand, the pointer returned by MPI
  // doesn't seem to persist throughout the test.
  // As a workaround, use mpi_ptr as the argument and then assign mpi_rank
  // to its value.
  MPI_Comm_rank(world_comm, &mpi_ptr);
  mpi_rank = mpi_ptr;

  start = clock();

  MDI_Send_Command("MD_INIT", mm_comm);

  for (int iiter = 0; iiter < niterations; iiter++) {
    MDI_Send_Command("<ENERGY", mm_comm);
    MDI_Recv(&energy, 1, MDI_DOUBLE, mm_comm);

    MDI_Send_Command("TIMESTEP", mm_comm);

    cout << "timestep: " << iiter << " " << energy << endl;
  }

  end = clock();
  cpu_time = ((double) (end - start)) / CLOCKS_PER_SEC;

  if ( mpi_rank == 0 ) {
    printf("Total time: %f\n",cpu_time);
  }

  MDI_Send_Command("EXIT", mm_comm);

  MPI_Barrier(world_comm);

  return 0;
}
