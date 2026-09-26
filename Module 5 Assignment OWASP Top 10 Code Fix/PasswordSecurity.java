import org.mindrot.jbcrypt.BCrypt;

public class PasswordSecurity {

    // hash a password when creating an account
    public static String hashPassword(
            String password) {
            
        return BCrypt.hashpw(
            password,
            BCrypt.gensalt(12)
        );
    }
    
    // Verify a password during login
    public static boolean verifyPassword(
            String inputPassword,
            String storeHash) {

        return BCrypt.checkpw(
            inputPassword,
            storeHash
        );
    }
}