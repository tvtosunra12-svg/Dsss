‎<?php
‎$server = "localhost";
‎$dbName = "logindb_ds";
‎$username = "root";
‎$password = "";
‎
‎$dsn = "mysql:host=$server;dbname=$dbName;charset=utf8mb4";
‎
‎try {
‎    $pdo = new PDO($dsn, $username, $password);
‎    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
‎
‎    // Database connection successful
‎} catch (PDOException $e) {
‎    die("Database connection failed.");
‎}
‎?>
‎
‎2nd
‎
‎
‎<?php
‎session_start();
‎
‎$errorMessage = "";
‎$userInput = "";
‎
‎if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["logout"])) {
‎    $_SESSION = [];
‎    session_destroy();
‎
‎    header("Location: index.php");
‎    exit;
‎}
‎
‎if ($_SERVER["REQUEST_METHOD"] == "POST") {
‎    $userInput = trim($_POST["username"] ?? "");
‎    $userPassword = $_POST["password"] ?? "";
‎
‎    if (empty($userInput) || empty($userPassword)) {
‎        $errorMessage = "Please fill in both fields.";
‎    } else {
‎        try {
‎            require_once __DIR__ . "/connection.php";
‎
‎            $query = "SELECT password FROM login WHERE username = :user LIMIT 1";
‎            $stmt = $pdo->prepare($query);
‎            $stmt->bindParam(":user", $userInput);
‎            $stmt->execute();
‎
‎            $passwordFromDB = $stmt->fetchColumn();
‎
‎            if ($passwordFromDB !== false && $passwordFromDB === $userPassword) {
‎                session_regenerate_id(true);
‎                $_SESSION["logged_in_user"] = $userInput;
‎            } else {
‎                $errorMessage = "Incorrect username or password.";
‎            }
‎        } catch (PDOException $e) {
‎            $errorMessage = "Login failed. Please check your database connection.";
‎        }
‎    }
‎}
‎
‎$currentUser = $_SESSION["logged_in_user"] ?? "";
‎?>
‎
‎<!DOCTYPE html>
‎<html lang="en">
‎<head>
‎    <meta charset="UTF-8">
‎    <meta name="viewport" content="width=device-width, initial-scale=1.0">
‎    <title>User Login</title>
‎    <link rel="stylesheet" href="style.css">
‎</head>
‎<body>
‎    <main>
‎        <?php if ($currentUser !== ""): ?>
‎            <h1>Welcome!</h1>
‎
‎            <p class="message">
‎                You are logged in as
‎                <?php echo htmlspecialchars($currentUser, ENT_QUOTES, "UTF-8"); ?>.
‎            </p>
‎
‎            <form method="post">
‎                <button type="submit" name="logout" value="1">
‎                    Sign Out
‎                </button>
‎            </form>
‎
‎        <?php else: ?>
‎            <h1>Member Login</h1>
‎            <p>Enter your account details to continue.</p>
‎
‎            <form method="post">
‎                <label for="username">Username</label>
‎                <input
‎                    type="text"
‎                    id="username"
‎                    name="username"
‎                    autocomplete="username"
‎                    required
‎                    value="<?php echo htmlspecialchars($userInput, ENT_QUOTES, "UTF-8"); ?>"
‎                >
‎
‎                <label for="password">Password</label>
‎                <input
‎                    type="password"
‎                    id="password"
‎                    name="password"
‎                    autocomplete="current-password"
‎                    required
‎                >
‎
‎                <?php if ($errorMessage !== ""): ?>
‎                    <p class="message error" role="alert">
‎                        <?php echo htmlspecialchars($errorMessage, ENT_QUOTES, "UTF-8"); ?>
‎                    </p>
‎                <?php endif; ?>
‎
‎                <button type="submit">Sign In</button>
‎            </form>
‎        <?php endif; ?>
‎    </main>
‎</body>
‎</html>
‎
‎3rd
‎
‎
‎:root {
‎    color-scheme: light;
‎    font-family: Arial, Helvetica, sans-serif;
‎    background: #f0f2f5;
‎    color: #222;
‎}
‎
‎* {
‎    box-sizing: border-box;
‎}
‎
‎body {
‎    min-height: 100vh;
‎    margin: 0;
‎    padding: 20px;
‎    display: flex;
‎    justify-content: center;
‎    align-items: center;
‎    background: #f0f2f5;
‎}
‎
‎main {
‎    width: 100%;
‎    max-width: 400px;
‎    padding: 32px;
‎    background: #ffffff;
‎    border: 1px solid #e0e0e0;
‎    border-radius: 12px;
‎    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
‎}
‎
‎h1 {
‎    margin: 0 0 10px;
‎    font-size: 26px;
‎    color: #263238;
‎}
‎
‎p {
‎    color: #666666;
‎    line-height: 1.6;
‎}
‎
‎label {
‎    display: block;
‎    margin: 18px 0 8px;
‎    font-size: 14px;
‎    font-weight: bold;
‎}
‎
‎input {
‎    width: 100%;
‎    min-height: 45px;
‎    padding: 11px 12px;
‎    border: 1px solid #cccccc;
‎    border-radius: 6px;
‎    font-size: 15px;
‎    background-color: #fafafa;
‎}
‎
‎input:focus {
‎    outline: 2px solid #bbdefb;
‎    border-color: #1976d2;
‎    background-color: #ffffff;
‎}
‎
‎button {
‎    width: 100%;
‎    min-height: 45px;
‎    margin-top: 22px;
‎    border: none;
‎    border-radius: 6px;
‎    background-color: #1976d2;
‎    color: #ffffff;
‎    font-size: 16px;
‎    font-weight: bold;
‎    cursor: pointer;
‎    transition: background-color 0.2s ease;
‎}
‎
‎button:hover {
‎    background-color: #125ca1;
‎}
‎
‎.message {
‎    margin: 16px 0 0;
‎}
‎
‎.error {
‎    color: #d32f2f;
‎}
‎