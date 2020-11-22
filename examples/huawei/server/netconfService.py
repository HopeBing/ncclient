from concurrent import futures
import logging

import grpc
import time

import netconfService_pb2
import netconfService_pb2_grpc

import sys
from ncclient import manager
from ncclient import operations

def huawei_connect(host, port, user, password):
    return manager.connect(host=host,
                           port=port,
                           username=user,
                           password=password,
                           hostkey_verify = False,
                           device_params={'name': "huawei"},
                           allow_agent = False,
                           look_for_keys = False)

def test_connect(host, port, user, password):
    with huawei_connect(host=host, port=port, user=user, password=password) as m:

        n = m._session.id
        print("The session id is %s." % (n))
        return n;

class Netconf(netconfService_pb2_grpc.NetconfServicer):

    def sayHello(self, request, context):
        netconfResult = test_connect('192.168.1.253', '830', 'huawei2', 'Huawei@2020');
        return netconfService_pb2.HelloReply(message='Hello, %s sessionId: %s!' % request.name % netconfResult)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    netconfService_pb2_grpc.add_NetconfServicer_to_server(Netconf(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server started\n")
    #server.wait_for_termination()
    #start() 不会阻塞，如果运行时你的代码没有其它的事情可做，你可能需要循环等待。
    try:
        while True:
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        server.stop(0);



if __name__ == '__main__':
    logging.basicConfig()
    serve()
