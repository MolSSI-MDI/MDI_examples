#location of required codes
LAMMPS_LOC=$(cat ../locations/lammps)
QE_LOC=$(cat ../locations/qe)

#remove old files
./clean.sh

#launch QE
cd qm
HOSTNAME=| hostname
${QE_LOC} -ipi "$HOSTNAME":8021 -mdi_name QM -in water.in > water.out &
cd ../

#launch LAMMPS
cd mm
${LAMMPS_LOC} -mdi "-role ENGINE -name MM -method TCP -port 8021 -hostname localhost" -in water.in > input.out &
cd ../

#launch QMMM
cd ../../MDI_examples/; python aimd.py &

wait
