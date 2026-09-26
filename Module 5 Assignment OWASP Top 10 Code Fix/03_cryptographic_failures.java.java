import java.security.SecureRandom;
import java.util.Base64;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;

public String hashPassword(String password)
        throws Exception {
        
    // generate a unique random salt.
    byte[] salt = new byte[16];
    new SecureRandom().nextBytes(salt);

    // use a password specific hashing algorithm.
    PBEKeySpec spec = new PBEKeySpec(
        password.toCharArray(),
        salt,
        600000,
        256
    );

    try {
        SecretKeyFactory factory = 
            SecretKeyFactory.getInstance(
                "PBKDF2WithHmacSHA256"
            );
        
        byte[] hash = factory
            .generateSecret(spec)
            .getEncoded();
        
        // store the algorithm settings, salt and hash.
        return "pbkdf2_sha256$600000$"
            + Base64.getEncoder().encodeToString(salt)
            + "$"
            + Base64.getEncoder().encodeToString(hash);
    
    } finally {
        spec.clearPassword();
    }
}