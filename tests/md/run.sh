#remove old files
./clean.sh

#launch LAMMPS
cd mm
/Users/tbarnes/Documents/mdi/lammps/src/lmp_mac -in water.in > input.out &
cd ../

#launch QMMM
cd ../../../controller/; python md.py &

wait
