#location of required codes
LAMMPS_LOC=$(cat ../locations/lammps)

#remove old files
./clean.sh

#launch LAMMPS
cd mm
${LAMMPS_LOC} -in water.in > input.out &
cd ../

#launch driver
cd ../../MDI_examples/; python md.py &

wait
