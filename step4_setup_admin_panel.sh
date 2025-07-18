#!/bin/bash
echo "🖥️ Creating Admin Panel PHP scripts..."

# auth.php
cat << 'PHP' > auth.php
<?php
session_start();
if (!isset($_SESSION['admin_logged_in'])) {
    header("Location: login.php");
    exit;
}
?>
PHP

# login.php
cat << 'PHP' > login.php
<?php
session_start();
$db = new PDO('sqlite:verifyme.sqlite');
$message = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];
    $stmt = $db->prepare("SELECT * FROM admin WHERE username = ?");
    $stmt->execute([$username]);
    $admin = $stmt->fetch(PDO::FETCH_ASSOC);
    if ($admin && password_verify($password, $admin['password'])) {
        $_SESSION['admin_logged_in'] = true;
        header("Location: dashboard.php");
        exit;
    } else {
        $message = "Invalid login.";
    }
}
?>
<form method="POST">
    <input type="text" name="username" placeholder="Username" required><br>
    <input type="password" name="password" placeholder="Password" required><br>
    <button type="submit">Login</button>
</form>
<?php if ($message) echo "<p>$message</p>"; ?>
PHP

# dashboard.php
cat << 'PHP' > dashboard.php
<?php
include 'auth.php';
$db = new PDO('sqlite:verifyme.sqlite');
$users = $db->query("SELECT * FROM users ORDER BY created_at DESC")->fetchAll(PDO::FETCH_ASSOC);
?>
<h2>✅ Verified ID Submissions</h2>
<a href="logout.php">Logout</a>
<table border="1" cellpadding="5" cellspacing="0">
<tr><th>ID</th><th>Username</th><th>Email</th><th>Status</th><th>Notes</th><th>ID Image</th></tr>
<?php foreach ($users as $user): ?>
<tr>
    <td><?= htmlspecialchars($user['id']) ?></td>
    <td><?= htmlspecialchars($user['username']) ?></td>
    <td><?= htmlspecialchars($user['email']) ?></td>
    <td><?= htmlspecialchars($user['status']) ?></td>
    <td><?= htmlspecialchars($user['notes']) ?></td>
    <td><img src="<?= htmlspecialchars($user['id_image']) ?>" alt="ID Image" width="100"></td>
</tr>
<?php endforeach; ?>
</table>
PHP

# logout.php
cat << 'PHP' > logout.php
<?php
session_start();
session_destroy();
header("Location: login.php");
exit;
?>
PHP

echo "✅ Admin panel scripts created: login.php, auth.php, dashboard.php, logout.php"
