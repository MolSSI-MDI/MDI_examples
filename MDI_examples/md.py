import sys
sys.path.insert(0, '../lib/mdi_build/molssi_driver_interface')

import mdi_python as mdi

niterations = 1000

# initialize the socket
sockfd = mdi.MDI_Init(8021)

# connect to the production codes
ncodes = 1
for icode in range(ncodes):
    comm = mdi.MDI_Accept_Connection(sockfd)

    # get the name of the code
    mdi.MDI_Send_Command("<NAME", comm)
    name = mdi.MDI_Recv(mdi.MDI_NAME_LENGTH, mdi.MDI_CHAR, comm)
    print('Received connection: ' + str(name))

    if name.strip() == 'MM':
        mm_comm = comm
    else:
        raise ValueError('Production code name not recognized')



# have the MD code initialize a new MD simulation
mdi.MDI_Send_Command("MD_INIT", mm_comm)

for iiter in range(niterations):

    # get the MM energy
    mdi.MDI_Send_Command("<ENERGY", mm_comm)
    mm_energy = mdi.MDI_Recv(1, mdi.MDI_DOUBLE, mm_comm)

    # do an MD timestep
    mdi.MDI_Send_Command("TIMESTEP", mm_comm)

    print("-------------------------------------")
    print("timestep: " + str(iiter))
    print("   MM Energy: " + str(mm_energy))


# close the production codes
mdi.MDI_Send_Command("EXIT", mm_comm)
