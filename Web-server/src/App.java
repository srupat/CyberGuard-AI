import java.io.*;
import java.net.*;

public class App {

    public static void main(String[] args) {
        int port = 8080; // The port number the server will listen on

        try (ServerSocket serverSocket = new ServerSocket(port)) {
            System.out.println("Server is listening on port " + port);

            while (true) {
                Socket clientSocket = serverSocket.accept();
                new Thread(new ClientHandler(clientSocket)).start();
            }
        } catch (IOException e) {
            System.out.println("Server exception: " + e.getMessage());
        }
    }
}

class ClientHandler implements Runnable {
    private Socket clientSocket;

    public ClientHandler(Socket socket) {
        this.clientSocket = socket;
    }

    @Override
    public void run() {
        try (BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                OutputStream clientOutput = clientSocket.getOutputStream();
                PrintWriter out = new PrintWriter(clientOutput, true)) {

            // Read the first line of the request (request method and path)
            String requestLine = in.readLine();
            System.out.println("Request: " + requestLine);

            if (requestLine != null && !requestLine.isEmpty()) {
                String[] requestParts = requestLine.split(" ");
                String method = requestParts[0];

                if ("GET".equalsIgnoreCase(method)) {
                    handleGetRequest(out);
                } else if ("POST".equalsIgnoreCase(method)) {
                    handlePostRequest(in, out);
                } else {
                    sendNotFound(out);
                }
            }
        } catch (IOException e) {
            System.out.println("Client handling error: " + e.getMessage());
        }
    }

    private void handleGetRequest(PrintWriter out) {
        out.println("HTTP/1.1 200 OK");
        out.println("Content-Type: text/html");
        out.println("Connection: close");
        out.println();
        out.println("<html><body><h1>GET request received</h1></body></html>");
        out.flush();
    }

    private void handlePostRequest(BufferedReader in, PrintWriter out) throws IOException {
        // Read headers
        String line;
        int contentLength = 0;
        while (!(line = in.readLine()).isEmpty()) {
            if (line.startsWith("Content-Length:")) {
                contentLength = Integer.parseInt(line.split(" ")[1]);
            }
        }

        // Read the body (post data)
        char[] body = new char[contentLength];
        in.read(body, 0, contentLength);

        String postData = new String(body);
        System.out.println("Post data: " + postData);

        out.println("HTTP/1.1 200 OK");
        out.println("Content-Type: text/html");
        out.println("Connection: close");
        out.println();
        out.println("<html><body><h1>POST request received</h1>");
        out.println("<p>Data: " + postData + "</p>");
        out.println("</body></html>");
        out.flush();
    }

    private void sendNotFound(PrintWriter out) {
        out.println("HTTP/1.1 404 Not Found");
        out.println("Content-Type: text/html");
        out.println("Connection: close");
        out.println();
        out.println("<html><body><h1>404 - Not Found</h1></body></html>");
        out.flush();
    }
}
