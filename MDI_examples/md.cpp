#include <iostream>
#include <stdio.h>
#include <time.h>
#include <string.h>
#include <mpi.h>
extern "C" {
#include "../lib/mdi_build/MDI_Library/mdi.h"
}

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

  // Initialize the MDI driver
  world_comm = MPI_COMM_WORLD;
  int ret = MDI_Init(argv[iarg+1], &world_comm);

  // Accept a communicator from the production code
  int mm_comm = MDI_Accept_Communicator();

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

  cout << "Total time: " << cpu_time << endl;

  MDI_Send_Command("EXIT", mm_comm);

  MPI_Barrier(world_comm);

  return 0;
}
