import java.io.*;
import java.net.*;
import java.util.HashMap;
import java.util.Map;
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
    private static Map<String, String> dataStore = new HashMap<>(); // In-memory data store

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
                String path = requestParts[1];

                if ("GET".equalsIgnoreCase(method)) {
                    handleGetRequest(path, out);
                } else if ("POST".equalsIgnoreCase(method)) {
                    handlePostRequest(path, in, out);
                } else if ("PUT".equalsIgnoreCase(method)) {
                    handlePutRequest(path, in, out);
                } else if ("PATCH".equalsIgnoreCase(method)) {
                    handlePatchRequest(path, in, out);
                } else if ("DELETE".equalsIgnoreCase(method)) {
                    handleDeleteRequest(path, out);
                } else {
                    sendNotFound(out);
                }
            }
        } catch (IOException e) {
            System.out.println("Client handling error: " + e.getMessage());
        }
    }

    private void handleGetRequest(String path, PrintWriter out) {
        String resource = getResourceFromPath(path);
        if (dataStore.containsKey(resource)) {
            String data = dataStore.get(resource);
            out.println("HTTP/1.1 200 OK");
            out.println("Content-Type: text/html");
            out.println("Connection: close");
            out.println();
            out.println("<html><body><h1>GET request received</h1>");
            out.println("<p>Resource: " + resource + "</p>");
            out.println("<p>Data: " + data + "</p>");
            out.println("</body></html>");
        } else {
            sendNotFound(out);
        }
        out.flush();
    }

    private void handlePostRequest(String path, BufferedReader in, PrintWriter out) throws IOException {
        String resource = getResourceFromPath(path);
        String postData = readRequestBody(in);
        dataStore.put(resource, postData); // Store the data with the resource as the key

        out.println("HTTP/1.1 201 Created");
        out.println("Content-Type: text/html");
        out.println("Connection: close");
        out.println();
        out.println("<html><body><h1>POST request received</h1>");
        out.println("<p>Resource: " + resource + "</p>");
        out.println("<p>Data: " + postData + "</p>");
        out.println("</body></html>");
        out.flush();
    }

    private void handlePutRequest(String path, BufferedReader in, PrintWriter out) throws IOException {
        String resource = getResourceFromPath(path);
        String putData = readRequestBody(in);
        if (dataStore.containsKey(resource)) {
            dataStore.put(resource, putData); // Update the data in memory

            out.println("HTTP/1.1 200 OK");
            out.println("Content-Type: text/html");
            out.println("Connection: close");
            out.println();
            out.println("<html><body><h1>PUT request received</h1>");
            out.println("<p>Resource: " + resource + "</p>");
            out.println("<p>Data: " + putData + "</p>");
            out.println("</body></html>");
        } else {
            sendNotFound(out);
        }
        out.flush();
    }

    private void handlePatchRequest(String path, BufferedReader in, PrintWriter out) throws IOException {
        String resource = getResourceFromPath(path);
        String patchData = readRequestBody(in);
        if (dataStore.containsKey(resource)) {
            dataStore.put(resource, patchData); // Update the data in memory

            out.println("HTTP/1.1 200 OK");
            out.println("Content-Type: text/html");
            out.println("Connection: close");
            out.println();
            out.println("<html><body><h1>PATCH request received</h1>");
            out.println("<p>Resource: " + resource + "</p>");
            out.println("<p>Data: " + patchData + "</p>");
            out.println("</body></html>");
        } else {
            sendNotFound(out);
        }
        out.flush();
    }

    private void handleDeleteRequest(String path, PrintWriter out) {
        String resource = getResourceFromPath(path);
        if (dataStore.containsKey(resource)) {
            dataStore.remove(resource); // Remove the data from memory

            out.println("HTTP/1.1 200 OK");
            out.println("Content-Type: text/html");
            out.println("Connection: close");
            out.println();
            out.println("<html><body><h1>DELETE request received</h1>");
            out.println("<p>Resource: " + resource + " deleted.</p>");
            out.println("</body></html>");
        } else {
            sendNotFound(out);
        }
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

    private String readRequestBody(BufferedReader in) throws IOException {
        StringBuilder body = new StringBuilder();
        String line;
        int contentLength = 0;

        while (!(line = in.readLine()).isEmpty()) {
            if (line.startsWith("Content-Length:")) {
                contentLength = Integer.parseInt(line.split(" ")[1]);
            }
        }

        char[] charArray = new char[contentLength];
        in.read(charArray, 0, contentLength);
        body.append(charArray);

        return body.toString();
    }

    private String getResourceFromPath(String path) {
        // Assuming path is something like "/resource1", this method returns "resource1"
        return path.startsWith("/") ? path.substring(1) : path;
    }
}
