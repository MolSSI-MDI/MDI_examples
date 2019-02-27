import sys
sys.path.insert(0, '../lib/mdi_build/molssi_driver_interface')

import mdi as mdi

niterations = 10

# initialize the socket
mdi.MDI_Init("-role DRIVER -name driver -method TCP -port 8021 -hostname localhost",None)

# connect to the production codes
ncodes = 2
for icode in range(ncodes):
    comm = mdi.MDI_Accept_Communicator()

    # get the name of the code
    mdi.MDI_Send_Command("<NAME", comm)
    name = mdi.MDI_Recv(mdi.MDI_NAME_LENGTH, mdi.MDI_CHAR, comm)
    print('Received connection: ' + str(name))

    if name.strip() == 'QM':
        qm_comm = comm
    elif name.strip() == 'MM':
        mm_comm = comm
    else:
        raise ValueError('Production code name not recognized')


# receive the number of atoms from the MM code
mdi.MDI_Send_Command("<NATOMS", mm_comm)
natom = mdi.MDI_Recv(1, mdi.MDI_INT, mm_comm)

# have the MD code initialize a new MD simulation
mdi.MDI_Send_Command("MD_INIT", mm_comm)

for iiter in range(niterations):

    # receive the coordinates from the MM code
    mdi.MDI_Send_Command("<COORDS", mm_comm)
    coords = mdi.MDI_Recv(3*natom, mdi.MDI_DOUBLE, mm_comm)

    # send the coordinates to the QM code
    mdi.MDI_Send_Command(">COORDS", qm_comm)
    mdi.MDI_Send(coords, 3*natom, mdi.MDI_DOUBLE, qm_comm)

    # run an SCF calculation
    mdi.MDI_Send_Command("SCF", qm_comm)

    # get the QM energy
    mdi.MDI_Send_Command("<ENERGY", qm_comm)
    qm_energy = mdi.MDI_Recv(1, mdi.MDI_DOUBLE, qm_comm)

    # get the MM energy
    mdi.MDI_Send_Command("<ENERGY", mm_comm)
    mm_energy = mdi.MDI_Recv(1, mdi.MDI_DOUBLE, mm_comm)

    # get the QM forces
    mdi.MDI_Send_Command("<FORCES", qm_comm)
    forces = mdi.MDI_Recv(3*natom, mdi.MDI_DOUBLE, qm_comm)

    # send the QM forces to the MM code
    mdi.MDI_Send_Command(">FORCES", mm_comm)
    mdi.MDI_Send(forces, 3*natom, mdi.MDI_DOUBLE, mm_comm)

    # do an MD timestep
    mdi.MDI_Send_Command("TIMESTEP", mm_comm)

    print("-------------------------------------")
    print("timestep: " + str(iiter))
    print("   QM Energy: " + str(qm_energy))
    print("   MM Energy: " + str(mm_energy))


# close the production codes
mdi.MDI_Send_Command("EXIT", qm_comm)
mdi.MDI_Send_Command("EXIT", mm_comm)
