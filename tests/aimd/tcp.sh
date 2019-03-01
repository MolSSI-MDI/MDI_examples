#location of required codes
LAMMPS_LOC=$(cat ../locations/lammps)
QE_LOC=$(cat ../locations/qe)

#remove old files
./clean.sh

#launch QE
cd qm
HOSTNAME=| hostname
${QE_LOC} -mdi "-role ENGINE -name QM -method TCP -port 8021 -hostname localhost" -mdi_name QM -in water.in > water.out &
cd ../

#launch LAMMPS
cd mm
${LAMMPS_LOC} -mdi "-role ENGINE -name MM -method TCP -port 8021 -hostname localhost" -in water.in > input.out &
cd ../

#launch driver
../../build/aimd -mdi "-role DRIVER -name driver -method TCP -port 8021" &

wait
