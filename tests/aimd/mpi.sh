#location of required codes
LAMMPS_LOC=$(cat ../locations/lammps)

#remove old files
./clean.sh

#launch LAMMPS
cd mm
mpiexec -n 1 ../../../build/aimd -mdi "-role DRIVER -name driver -method MPI" : \
    -n 1 ${LAMMPS_LOC} -mdi "-role ENGINE -name MM -method MPI" -in water.in > input.out



wait
