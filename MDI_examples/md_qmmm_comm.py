# This is an MD calculation, identical to md.py, except that it includes additional commands to test efficiency

import sys
sys.path.insert(0, '../lib/mdi_build/molssi_driver_interface')

import mdi as mdi

niterations = 1000

# initialize the socket
mdi.MDI_Init("-role DRIVER -name driver -method TCP -port 8021 -hostname localhost",None)

# connect to the production codes
ncodes = 1
for icode in range(ncodes):
    comm = mdi.MDI_Accept_Communicator()

    # get the name of the code
    mdi.MDI_Send_Command("<NAME", comm)
    name = mdi.MDI_Recv(mdi.MDI_NAME_LENGTH, mdi.MDI_CHAR, comm)
    print('Received connection: ' + str(name))

    if name.strip() == 'MM':
        mm_comm = comm
    else:
        raise ValueError('Production code name not recognized')


# receive the number of atoms
mdi.MDI_Send_Command("<NATOMS", mm_comm)
natoms = mdi.MDI_Recv(1, mdi.MDI_INT, mm_comm)

# receive the number of atom types
mdi.MDI_Send_Command("<NTYPES", mm_comm)
ntypes = mdi.MDI_Recv(1, mdi.MDI_INT, mm_comm)

# receive the atom types
mdi.MDI_Send_Command("<TYPES", mm_comm)
types = mdi.MDI_Recv(natoms, mdi.MDI_INT, mm_comm)

# have the MD code initialize a new MD simulation
mdi.MDI_Send_Command("MD_INIT", mm_comm)

update_forces = [ 0.0 for i in range(3*natoms) ]

for iiter in range(niterations):

    # receive the cell dimensions
    mdi.MDI_Send_Command("<CELL", mm_comm)
    cell = mdi.MDI_Recv(9, mdi.MDI_DOUBLE, mm_comm)

    # receive the coordinates
    mdi.MDI_Send_Command("<COORDS", mm_comm)
    coords = mdi.MDI_Recv(3*natoms, mdi.MDI_DOUBLE, mm_comm)

    # receive the charges
    mdi.MDI_Send_Command("<CHARGES", mm_comm)
    charges = mdi.MDI_Recv(natoms, mdi.MDI_DOUBLE, mm_comm)

    # receive the charges
    mdi.MDI_Send_Command("<MASSES", mm_comm)
    masses = mdi.MDI_Recv(ntypes+1, mdi.MDI_DOUBLE, mm_comm)

    # get the MM energy
    mdi.MDI_Send_Command("<ENERGY", mm_comm)
    mm_energy = mdi.MDI_Recv(1, mdi.MDI_DOUBLE, mm_comm)

    # send a set of updated forces
    mdi.MDI_Send_Command("+PRE-FORCES", mm_comm)
    mdi.MDI_Send(update_forces, 3*natoms, mdi.MDI_DOUBLE, mm_comm)

    # do an MD timestep
    mdi.MDI_Send_Command("TIMESTEP", mm_comm)

    print("-------------------------------------")
    print("timestep: " + str(iiter))
    print("   MM Energy: " + str(mm_energy))


# close the production codes
mdi.MDI_Send_Command("EXIT", mm_comm)
