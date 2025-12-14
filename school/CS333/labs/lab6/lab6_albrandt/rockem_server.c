// Lex Albrandt
// CS333
// Lab6

// System includes
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/uio.h>
#include <unistd.h>
#include <getopt.h>
#include <pthread.h>

// Local includes
#include "rockem_hdr.h"

// MACROS
#define LISTENQ 100

// Prototypes
void process_connection(int sockfd, void *buf, int n);
void *thread_get(void *p);
void *thread_put(void *p);
void *thread_dir(void *p);
void *server_commands(void *p);
void current_connections_inc(void);
void current_connections_dec(void);
unsigned int current_connections_get(void);
void server_help(void);

// Global variables
static short is_verbose = 0;
static int usleep_time = 0;
static long tcount = 0;
static int current_connections = 0;
static pthread_mutex_t connections_mutex = PTHREAD_MUTEX_INITIALIZER;


int main(int argc, char *argv[]) 
{
    int listenfd = 0;
    int sockfd = 0;
    int n = 0;
    char buf[MAXLINE] = {'\0'};
    socklen_t clilen;
    struct sockaddr_in cliaddr;
    struct sockaddr_in servaddr;
    short ip_port = DEFAULT_SERVER_PORT;
    pthread_t cmd_thread;

	{
		int opt = 0;

        // Getopt structure
		while ((opt = getopt(argc, argv, SERVER_OPTIONS)) != -1) {
			switch (opt) {
            
            // Define ip_port
			case 'p':
				// CONVERT and assign optarg to ip_port
                ip_port = (short) atoi(optarg);
				break;
            
            // Increment sleep time
			case 'u':
				// add 1000 to usleep_time
                usleep_time += USLEEP_INCREMENT;
				break;

            // Increment verbose
			case 'v':
				is_verbose++;
				break;

            // Print help info
			case 'h':
				fprintf(stderr, "%s ...\n\tOptions: %s\n"
						, argv[0], SERVER_OPTIONS);
				fprintf(stderr, "\t-p #\t\tport on which the server will listen (default %hd)\n"
						, DEFAULT_SERVER_PORT);
				fprintf(stderr, "\t-u\t\tnumber of thousands of microseconds the server will sleep between "
						"read/write calls (default %d)\n"
						, usleep_time);
				fprintf(stderr, "\t-v\t\tenable verbose output. Can occur more than once to increase output\n");
				fprintf(stderr, "\t-h\t\tshow this rather lame help message\n");
				exit(EXIT_SUCCESS);
				break;

            // Default
			default:
				fprintf(stderr, "*** Oops, something strange happened <%s> ***\n", argv[0]);
				break;
			}
		}
	}

    // Create a socket from the AF_INET family, that is a stream socket
    listenfd = socket(AF_INET, SOCK_STREAM, 0);
    memset(&servaddr, 0, sizeof(servaddr));

    // An IPv4 Address
    servaddr.sin_family = AF_INET;

    // Host-TO-Network-Long. Listen on any interface/IP of the system.
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY);

    // Host-TO-Network-Short, the default port from above.
    servaddr.sin_port = htons(ip_port);

    // bind the listenfd
    if (bind(listenfd, (struct sockaddr *) &servaddr, sizeof(servaddr)) != 0)
    {
        perror("bind not working");
        exit(EXIT_FAILURE);
    }

    // listen on the listenfd
    listen(listenfd, LISTENQ);


    // Output server info
    {
        char hostname[256] = {'\0'};
        struct hostent *host_entry = NULL;
        char *IPbuffer = NULL;

        memset(hostname, 0, sizeof(hostname));
        gethostname(hostname, sizeof(hostname));
        host_entry = gethostbyname(hostname);
        IPbuffer = inet_ntoa(*((struct in_addr*) host_entry->h_addr_list[0]));
        
        fprintf(stdout, "Hostname: %s\n", hostname);
        fprintf(stdout, "IP:       %s\n", IPbuffer);
        fprintf(stdout, "Port:     %d\n", ip_port);
		fprintf(stdout, "verbose     %d\n", is_verbose);
		fprintf(stdout, "usleep_time %d\n", usleep_time);
    }

    // create the input handler thread
    pthread_create(&cmd_thread, NULL, server_commands, NULL);

    // client length
    clilen = sizeof(cliaddr);

    // Accept connections on the listenfd
    for ( ; ; ) {
        // Accept connections to the socket
        sockfd = accept(listenfd, (struct sockaddr *) &cliaddr, &clilen);

        // You REALLY want to memset to all zeroes before you get bytes from
        // the socket.
        memset(buf, 0, sizeof(buf));

        // read a cmd_t structure from the socket.
        // if zro bytes are read, close the socket
        if ((n = read(sockfd, buf, sizeof(cmd_t))) == 0) {
            // Nothing was read, EOF
            fprintf(stdout, "EOF found on client connection socket, "
                    "closing connection.\n");
            close(sockfd);
        }

        else {
            if (is_verbose) {
                fprintf(stdout, "Connection from client: <%s>\n", buf);
            }
            // process the command from the client
            // in the process_connection() is where I divy out the put/get/dir
            // threads
            process_connection(sockfd, buf, n);
        }
        
    }

    printf("Closing listen socket\n");
    close(listenfd);

    return(EXIT_SUCCESS);
}


void process_connection(int sockfd, void *buf, int n)
{
    // I have to allocate one of these for each thread that is created.
    // The thread is responsible for calling free on it.
    cmd_t *cmd = (cmd_t *) malloc(sizeof(cmd_t));
    int ret;
    pthread_t tid;
    pthread_attr_t attr;

    (void)n;

    pthread_attr_init(&attr);
    pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED);

    memcpy(cmd, buf, sizeof(cmd_t));
    cmd->sock = sockfd;
    if (is_verbose) {
        fprintf(stderr, "Request from client: <%s> <%s>\n"
                , cmd->cmd, cmd->name);
    }

    if (strcmp(cmd->cmd, CMD_GET) == 0) {
        // create thread to handle get file
        ret = pthread_create(&tid, &attr, thread_get, cmd);
        if (ret < 0) {
            fprintf(stderr, "ERROR: %d\n", __LINE__);
        }
    }
    else if (strcmp(cmd->cmd, CMD_PUT) == 0) {
        // create thread to handle put file
        ret = pthread_create(&tid, &attr, thread_put, cmd);
        if (ret < 0) {
            fprintf(stderr, "ERROR: %d\n", __LINE__);
        }
    }
    else if (strcmp(cmd->cmd, CMD_DIR) == 0) {
        // create thread to handle dir
        ret = pthread_create(&tid, &attr, thread_dir, cmd);
        if (ret < 0) {
            fprintf(stderr, "ERROR: %d\n", __LINE__);
        }
    }
    else {
        // This should never happen since the checks are made on 
        // the client side.
        fprintf(stderr, "ERROR: unknown command >%s< %d\n", cmd->cmd, __LINE__);
        // close the socket
        close(sockfd);
    }
}


void * server_commands(void *p)
{
    char cmd[80] = {'\0'};
    char *ret_val = NULL;

    (void)p;

    // detach the thread
    pthread_detach(pthread_self());

    server_help();
    for ( ; ; ) {
        fputs(">> ", stdout);
        ret_val = fgets(cmd, sizeof(cmd), stdin);
        if (ret_val == NULL) {
            // end of input, a control-D was pressed.
            break;
        }
        // STOMP on the pesky new line
		cmd[strlen(cmd) - 1] = '\0';

        if (strlen(cmd) == 0) {
            continue;
        }
        else if (strcmp(cmd, SERVER_CMD_EXIT) == 0) {
            // I really should do something better than this.
            break;
        }
        else if (strcmp(cmd, SERVER_CMD_COUNT) == 0) {
            printf("total connections   %lu\n", tcount);
            printf("current connections %u\n", current_connections_get());
            printf("verbose             %d\n", is_verbose);
			printf("usleep_time         %d\n", usleep_time);
        }
        else if (strcmp(cmd, SERVER_CMD_VPLUS) == 0) {
            is_verbose++;
            printf("verbose set to %d\n", is_verbose);
        }
        else if (strcmp(cmd, SERVER_CMD_VMINUS) == 0) {
            is_verbose--;
            if (is_verbose < 0) {
                is_verbose = 0;
            }
            printf("verbose set to %d\n", is_verbose);
        }
        else if (strcmp(cmd, SERVER_CMD_UPLUS) == 0) {
			usleep_time += USLEEP_INCREMENT;
            printf("usleep_time set to %d\n", usleep_time);
        }
        else if (strcmp(cmd, SERVER_CMD_UMINUS) == 0) {
			usleep_time -= USLEEP_INCREMENT;
            if (usleep_time < 0) {
                usleep_time = 0;
            }
            printf("usleep_time set to %d\n", usleep_time);
        }
        else if (strcmp(cmd, SERVER_CMD_HELP) == 0) {
            server_help();
        }
        else {
            printf("command not recognized >>%s<<\n", cmd);
        }
    }

    // This is really harsh. It terminates on all existing threads.
    // This would probably be better with a good exit handler
    exit(EXIT_SUCCESS);
}


void server_help(void)
{
    printf("available commands are:\n");
    printf("\t%s : show the total connection count "
           "and number current connection\n"
           , SERVER_CMD_COUNT);
    printf("\t%s    : increment the is_verbose flag (current %d)\n"
           , SERVER_CMD_VPLUS, is_verbose);
    printf("\t%s    : decrement the is_verbose flag (current %d)\n"
           , SERVER_CMD_VMINUS, is_verbose);
	
    printf("\t%s    : increment the usleep_time variable (by %d, currently %d)\n"
           , SERVER_CMD_UPLUS, USLEEP_INCREMENT, usleep_time);
    printf("\t%s    : decrement the usleep_time variable (by %d, currently %d)\n"
           , SERVER_CMD_UMINUS, USLEEP_INCREMENT, usleep_time);
	
    printf("\t%s  : exit the server process\n"
           , SERVER_CMD_EXIT);
    printf("\t%s  : show this help\n"
           , SERVER_CMD_HELP);
}


void * thread_get(void *p)
{
    cmd_t *cmd = (cmd_t *) p;
    int fd = 0;
    ssize_t bytes_read = 0;
    char buffer[MAXLINE] = {'\0'};

    current_connections_inc();

    if (is_verbose) {
        fprintf(stderr, "Sending %s to client\n", cmd->name);
    }
    // ope the file in cmd->name, read-only
    fd = open(cmd->name, O_RDONLY);
    if (fd < 0)
    {
        perror("open");
        close(cmd->sock);
        free(cmd);
        current_connections_dec();
        pthread_exit((void *) EXIT_FAILURE);
    }

		
    // in a while loop, read from the file and write to the socket
    // within the while loop, if sleep_flap > 0, usleep()
    while ((bytes_read = read(fd, buffer, MAXLINE)) > 0)
    {
        write(cmd->sock, buffer, bytes_read);
        if (usleep_time > 0)
        {
            usleep(usleep_time);
        }
    }

    close(fd);
    close(cmd->sock);
    free(cmd);
    current_connections_dec();

    pthread_exit((void *) EXIT_SUCCESS);
}

void * thread_put(void *p)
{
    cmd_t *cmd = (cmd_t *) p;
    int fd = 0;
    ssize_t bytes_read = 0;
    char buffer[MAXLINE] = {'\0'};

    // Increment current connections
    current_connections_inc();

    if (is_verbose) {
        fprintf(stderr, "VERBOSE: Receiving %s from client\n"
                , cmd->name);
    }
    // open the file in cmd->name as write-only
    // truncate it if it aready exists
    fd = open(cmd->name, O_WRONLY | O_CREAT | O_TRUNC, 0644);

    if (fd < 0) {
        perror("open");
        close(cmd->sock);
        free(cmd);
        current_connections_dec();
        pthread_exit((void *) EXIT_FAILURE);
    }


    // in a while loop, read from the socket and write to the file
    // within the while loop, if sleep_flap > 0, usleep()
    while ((bytes_read = read(cmd->sock, buffer, MAXLINE)) > 0)
    {
        write(fd, buffer, bytes_read);
        if (usleep_time > 0)
        {
            usleep(usleep_time);
        }
    }


    close(fd);
    close(cmd->sock);
    free(cmd);
    current_connections_dec();

    pthread_exit((void *) EXIT_SUCCESS);
}


void * thread_dir(void *p)
{
    cmd_t *cmd = (cmd_t *) p;
    FILE *fp = NULL;
    char buffer[MAXLINE] = {'\0'};

    current_connections_inc();

    fp = popen("ls -la", "r");
    if (fp == NULL) {
        perror("popen");
        close(cmd->sock);
        free(cmd);
        current_connections_dec();
        pthread_exit((void *) EXIT_FAILURE);
    }
    memset(buffer, 0, sizeof(buffer));

    while (fgets(buffer, sizeof(buffer), fp) != NULL)
    {
        write(cmd->sock, buffer, strlen(buffer));
        if (usleep_time > 0)
        {
            usleep(usleep_time);
        }
    }

    pclose(fp);
    close(cmd->sock);
    free(cmd);
    current_connections_dec();

    pthread_exit((void *) EXIT_SUCCESS);
}


void current_connections_inc(void)
{
    // lock
    pthread_mutex_lock(&connections_mutex);
    // increment both values
    tcount++;
    current_connections++;
    // unlock
    pthread_mutex_unlock(&connections_mutex);
}

void current_connections_dec(void)
{
    // lock
    pthread_mutex_lock(&connections_mutex);
    // decrement one value
    current_connections--;
    // unlock
    pthread_mutex_unlock(&connections_mutex);
}

unsigned int current_connections_get(void)
{
    unsigned int count;
    pthread_mutex_lock(&connections_mutex);
    count = current_connections;
    pthread_mutex_unlock(&connections_mutex);
    return count;
}
