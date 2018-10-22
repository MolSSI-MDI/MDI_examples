#remove old files
./clean.sh

#launch LAMMPS
cd mm
/Users/tbarnes/Documents/mdi/lammps/src/lmp_mac -in water.in > input.out &
cd ../

#launch the driver
cd ../../MDI_examples/; python md_qmmm_comm.py &

wait
