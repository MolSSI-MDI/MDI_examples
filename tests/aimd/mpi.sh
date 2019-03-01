#location of required codes
LAMMPS_LOC=$(cat ../locations/lammps)
QE_LOC=$(cat ../locations/qe)

#remove old files
./clean.sh

#launch LAMMPS
cd data
mpiexec -n 1 ../../../build/aimd -mdi "-role DRIVER -name driver -method MPI" : \
    -n 1 ${LAMMPS_LOC} -mdi "-role ENGINE -name MM -method MPI" -in water.in > input.out : \
    -n 8 ${QE_LOC} -mdi "-role ENGINE -name QM -method MPI" -mdi_name QM -in qe.in > qe.out



wait
