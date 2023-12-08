from mpi4py import MPI
import time
comm = MPI.COMM_WORLD
comm_rank = comm.Get_rank()
comm_size = comm.Get_size()

data_send = comm_rank
if comm_rank == 0:
    comm.isend(data_send+1, dest=(comm_rank + 1) % comm_size)
    comm.isend(data_send-1, dest=(comm_rank - 1) % comm_size)
    comm.isend(data_send, dest=(comm_rank + 1) % comm_size)
    comm.isend(data_send, dest=(comm_rank - 1) % comm_size)
    data_recv1 = comm.recv(source=(comm_rank - 1) % comm_size)
    data_recv2 = comm.recv(source=(comm_rank + 1) % comm_size)
    print(data_recv1)
    print(data_recv2)
    data_recv1 = comm.recv(source=(comm_rank - 1) % comm_size)
    data_recv2 = comm.recv(source=(comm_rank + 1) % comm_size)
    print(data_recv1)
    print(data_recv2)
if comm_rank > 0:
    time.sleep(2)
    comm.isend(data_send + 1, dest=(comm_rank + 1) % comm_size)
    comm.isend(data_send - 1, dest=(comm_rank - 1) % comm_size)
    comm.isend(data_send, dest=(comm_rank + 1) % comm_size)
    comm.isend(data_send, dest=(comm_rank - 1) % comm_size)
    data_recv1 = comm.recv(source=(comm_rank - 1) % comm_size)
    data_recv2 = comm.recv(source=(comm_rank + 1) % comm_size)

time.sleep(2)
print("my rank is %d, I received: %s %s" % (comm_rank, data_recv1,data_recv2))
