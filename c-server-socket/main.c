#include "../c-socketUtils/socketutil.h"

int main() {
    
    int serverSocketFD = createTCPIpv4Socket();
    struct sockaddr_in* serverAddress = createIpv4Address("",  2000);

    int result = bind(serverSocketFD, (const struct sockaddr*)serverAddress, sizeof(*serverAddress));
    
    if (result == 0) {
        printf("socket was bound successfully\n");
    } else {
        perror("bind");
        return 1; // end program here if bind fail
    }

    int listen_result = listen(serverSocketFD, 10); // 10 is the size of the queue of incoming connection

    startAcceptingIncomingConnections(serverSocketFD);

    shutdown(serverSocketFD, SHUT_RDWR); // SHUT_RDWR is for shutting down the connection (Read and Write)
    close(serverSocketFD);
    free(serverAddress); // free the memory allocated for serverAddress

    return 0;
}