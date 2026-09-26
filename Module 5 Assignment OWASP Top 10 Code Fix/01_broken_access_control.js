const mongoose = require('mongoose');

// requireAuth must verify the session and set req user.
app.get('/profile/:userId', requireAuth, async (req, res) => {
    try {
        const requestedId = req.params.userId;

        // check whether the ID is valid.
        if (!mongoose.isValidObjectId(requestedId)) {
            return res.status(400).send('Invalid user ID');
        }

        // only allpw access to your own profile.
        if (String(req.user._id) !== requestedId) {
            return res.status(403).send('Access denied');
        }

        // return only safe profile fields.
        const user = await User.findById(requestedId)
            .select('username email');
        
        if (!user) {
            return res.status(404).send('User not found');
        }

        return res.json(user);
    } catch (error) {
        return res.status(500).send('Server error');
    }
});