# OWASP-Top-10-Code-Fix

This project identifies and corrects security vulnerabilities in ten code samples written in Python, Java, JavaScript, and HTML. Each example demonstrates a security issue related to the OWASP top 10.

1.	Broken Access Control – JavaScript

The original JavaScript code allows users to access any person’s profile by changing the user ID in the URL. The application does not verify that the person requesting the profile is authorized to view it. This vulnerability could allow attackers to access other users personal information.

I added authentication and an authorization check that compares the request profile ID with the authenticated user’s ID. I also included error handling and restricted the information returned by the application.

The corrected code requires users to be logged in and verifies that they are only requesting their own profile. If someone attempts to access another person’s account the application denies the request.

OWASP Refs: https://top10.owasp.org/2021/A01_2021-Broken_Access_Control/index.html



2.	Broken Access Control – Python

The original Python code retrieves account information using the user ID provided in the URL without verifying that the account belongs to the person making the request. An attacker could modify the user ID to access another person’s private account information.

I added Flask Login authentication and an authorization check that compares the requested account ID with the logged in user’s ID. I also included error handling for accounts that do not exist and limited the information returned.

The application now verifies the user’s identity before allowing access to account information. Requests for another person’s account are rejected with an HTTP 403 Forbidden response.

OWASP Refs: https://top10.owasp.org/2021/A01_2021-Broken_Access_Control/index.html



3.	Cryptographic Failures – Java

The original Java code uses MD5 to hash passwords. MD5 is an outdated, fast hashing algorithm that us unsuitable for password storage. If attackers obtain the password database, they could attempt to recover users passwords using automated password cracking tools.

I replaced MD5 with PBKDF2-HMAC-SHA256. I added a unique random salt for each password and configured the algorithm to use 600,000 iterations.

PBKDF2 makes password guessing more computationally expensive. The random salt ensures that identical passwords do not produce identical stored hashes. These changes make password cracking attacks more difficult if the password data is compromised.

OWASP Refs: https://top10.owasp.org/2021/A02_2021-Cryptographic_Failures/
https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html



4.	Cryptographic Failures – Python

The Original Python code uses SHA 1 to hash passwords. SHA 1 is unsuitable for password storage because it is computationally fast and the code does not use a random salt. If the database is compromised, attackers could attempt to crack users passwords.

I replaced SHA 1 with Argon2ID using the Python argon2-cffi library. I also added a function to verify passwords against their stored hashes.

Argon2id uses computationally expensive and memory intensive operations to make password cracking more difficult. It automatically generates a unique random salt for each password and allows the application to verify passwords without storing their original values.

OWASP Refs: https://top10.owasp.org/2021/A02_2021-Cryptographic_Failures/
https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html


5.	Injection – Java

The original Java code is vulnerable to SQL injection because it directly inserts user input into an SQL query. An attacker could provide malicious input that changes the meaning of the query, potentially allowing unauthorized access to database records or modification of stored information.

I replaced the original SQL statement with a parameterized query using Java’s PreparedStatment. Instead of combining user input with SQL commands, the corrected code uses a placeholder and the setString() method.

Parameterized queries separate user input from executable SQL commands. The database treates the supplied username as data rather than allowing it to change the SQL statement. This prevents the supplied suername from causing SQL injection.

OWASP Refs: https://top10.owasp.org/2021/A03_2021-Injection/
https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html


6.	Injection – JavaScript

The original JavaScript code is vulnerable to NoSQL injection because it passes unvalidated user input directly into a MongoDB query. An attacker could potentially submit MongoDB query operators instead of an ordinary username, allowing them to manipulate the query and retrieve unintended records. 

I added input validation to ensure the username is a string containing only permitted characters. I also added authentication, authorization checks and restrictions on which database fields can be returned.

Input validation prevents users from submitting unexpected data types, including objects containing MongoDB query operators. Authentication and authorization ensure that users can only retrieve records they are permitted to access.

OWASP Refs: https://top10.owasp.org/2021/A03_2021-Injection/


7.	Insecure Design – Python

The original password reset function allows someone to change an account’s password simply by providing an email address and a new password. The application does not verify account ownership, meaning an attacker who knows another person’s email address could potentially take control of their account. The original code also appears to store the new password without securely hashing it.

I redesigned the password reset process to user secure, randomly generated reset tokens sent to the account owner’s registered email address. The token expires after limited period and is deleted after it is used. I also added Argon2id password hashing before saving the new password.

The redesigned process requires a valid reset token before allowing a password change. The short expiration period and single use token reduce the risk of unauthorized password resets. Hashing the new password protects it if the database is compromised. A complete production implementation would also require rate limiting, atomic token redemption and invalidation of existing sessions after a successful password reset.

OWASP Refs: https://top10.owasp.org/2021/A04_2021-Insecure_Design/index.html
https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html


8.	Software and Data Integrity Failures – HTML

The original HTML code loads an external JavaScript library without verifying the integrity of the downloaded file. If an attacker compromises the library or its hosting service, malicious JavaScript could potentially execute in visitors browsers.

I added the Subresource integrity (SRI) attribute and the crossorigin attribute to the external script element. The SRI attribute must contain the correct SHA 384 hash of the trusted JavaScript file.

Subresource integrity allows the browser to verify that the downloaded JavaScript file matches the expected cryptographic hash. If someone modifies the external script, the browser detects the mismatch and refuses to execute it. The example must be configured with a real library URL and its matching hash before deployment.

OWASP Refs: https://top10.owasp.org/2021/A08_2021-Software_and_Data_Integrity_Failures/


9.	Server Side Request Forgery – Python

The original Python code allows users to enter any URL and directs the application to send an HTTP request to that address. This creates a server side request forgery vulnerability because attackers could potentially user the application to access internal network resources or services that are not publicly accessible.

I replaced unrestricted URL input with a predefined list of approved destinations. I also disabled automatic redirects, added a request timeout and included error handling for failed requests.

Restricting requests to approved destinations prevents users from freely specifying arbitrary URLs. Disabling redirects reduces the risk of an approved URL redirecting the application to an unauthorized address. The timeout prevents the application from waiting indefinitely for a response.

A production application should also enforce network level and DNS restriction to prevent requests from reaching prohibited internal services.

OWASP Refs: https://top10.owasp.org/2021/A10_2021-Server-Side_Request_Forgery_%28SSRF%29/
https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html


10.	 Identification and Authentication Failures – Java

The original Java code directly compares the password entered by a user with the password stored in the application. This suggests that passwords may be stored in plain text.  If attackers obtained the database, they could potentially steal users passwords and gain unauthorized access to their accounts. 

I replaced the direct password comparison with bcrypt password hashing and verification using the jBCrypt library. Passwords are hashed during account registration, and the application verifies entered passwords against the stored hashed during login.

Bcrypt uses random salts and a configurable work factor to make password cracking attacks more expensive. The application can securely verify passwords without storing their original plain text values.

OWASP Refs: https://top10.owasp.org/2021/A07_2021-Identification_and_Authentication_Failures/
https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html

