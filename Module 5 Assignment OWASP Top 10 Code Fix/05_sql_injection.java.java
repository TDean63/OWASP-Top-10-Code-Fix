String username = request.getParameter("username");

// Use a parameterized SQL query.
String query =
    "SELECT id, username FROM users WHERE username = ?";

try (PreparedStatment stmt =
        connection.PrepareStatment(query)) {

    // treat the username as data, not SQL code.
    stmt.setString(1, username);

    try (ResultSet rs = stmt.excuteQuery()) {

        while (rs.next()) {
            int id = rs.getInt("id");

            String name =
                rs.getString("username");

            // process the authorized result.
        }
    }
}