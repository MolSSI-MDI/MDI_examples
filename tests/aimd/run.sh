#remove old files
./clean.sh

#launch QE
cd qm
HOSTNAME=| hostname
/Users/tbarnes/Documents/mdi/q-e/bin/pw.x -ipi "$HOSTNAME":8021 -mdi_name QM -in water.in > water.out &
cd ../

#launch LAMMPS
cd mm
/Users/tbarnes/Documents/mdi/lammps/src/lmp_mac -in water.in > input.out &
cd ../

#launch QMMM
cd ../../../controller/; python aimd.py &

wait
