import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.net.InetAddress;
import java.net.Socket;
import java.net.URL;

public class TCPRequest {
    public static void main(String[] args) {
        connectToTCPServer("http://wireshark.grydeske.net");
    }

    private static void connectToTCPServer(String url) {
        Socket socket = null;
        PrintStream out = null;
        BufferedReader in = null;
        
        try {
            String host = new URL(url).getHost();
            InetAddress ia = InetAddress.getByName(host);
            String ip = ia.getHostAddress();
            socket = new Socket(ip,80);
            out = new PrintStream(socket.getOutputStream());
            in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

            out.println("GET / HTTP/1.1");
            out.println("Host: " + host);
            out.println("Connection: close");
            out.println(); //Empty line

            String line = in.readLine();
            while (line != null) {
                System.out.println(line);
                line = in.readLine();
            }
        }
        catch(IOException e) {
            e.printStackTrace();
        }
        finally {
            try {
                if(socket != null) socket.close();
                if(out != null) out.close();
                if(in != null) in.close();
            }
            catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}