#location of required codes
LAMMPS_LOC=$(cat ../locations/lammps)

#remove old files
./clean.sh

#launch LAMMPS
cd mm
mpiexec -n 1 ../../../build/md -mdi "-role DRIVER -name driver -method MPI" > ../output : \
    -n 1 ${LAMMPS_LOC} -mdi "-role ENGINE -name MM -method MPI" -in water.in > input.out



wait
