#location of required codes
LAMMPS_LOC=$(cat ../locations/lammps)

#remove old files
./clean.sh

#launch LAMMPS
cd mm
${LAMMPS_LOC} -in water.in > input.out &
cd ../

#launch the driver
cd ../../MDI_examples/; python md_qmmm_comm.py &

wait
