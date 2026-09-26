app.get('/user', requireAuth, async (req, res) => {
    try {
        const username = req.query.username;

        // accept only a single username string.
        if (
            typeof username !== 'string' ||
            username.length < 1 ||
            username.length > 50 ||
            !/^[a-zA-Z0-9 ]+$/.test(username)
        ) {
            return res.status(400).json({
                error: 'Invalid username'
            });
        }

        // restrict users to their own records.
        if (username !== req.user.username) {
            return res.status(403).json({
                error: 'Access denied'
            });
        }

        const user = await db
            .collection('users')
            .findOne(
                { username: username },
                {
                    projection: {
                        _id: 0,
                        username: 1
                    }
                }
            );
        
        if (!user) {
            return res.status(404).json({
                error: 'User not found'
            });
        }

        return res.json(user);

    } catch (error) {
        return res.status(500).json({
            error: 'Server error'
        });
    }
});