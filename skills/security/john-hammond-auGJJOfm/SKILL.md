markdown
# Retrieve-WiFi-Passwords-Securely

## Description
Extract wireless Wi-Fi network passwords securely using Rust, avoiding detection by EDR solutions.

## Body
### Step 1: Set Up the Environment
1. **Install Rust**: Download and install Rust from [rust-lang.org](https://www.rust-lang.org/).
2. **Set Up IDE**: Install an Integrated Development Environment (IDE) like Visual Studio Code with the Rust extension.
3. **Create a New Project**:
   - Open your terminal or command prompt.
   - Navigate to your desired project directory.
   - Run `cargo new wifi_pass_dump` to create a new Rust project named `wifi_pass_dump`.
   - Change into the project directory: `cd wifi_pass_dump`.

### Step 2: Write the Code
1. **Add Dependencies**: Open `Cargo.toml` and add necessary dependencies:
    ```toml
    [dependencies]
    winreg = "0.8"
    ```
2. **Implement the Main Function**:
   - Open `src/main.rs` and replace its content with the following code:
    ```rust
    use std::process::Command;
    use winreg::{enums::HKEY_CURRENT_USER, RegKey};

    fn main() {
        // Retrieve Wi-Fi profiles
        let hkcu = RegKey::predef(HKEY_CURRENT_USER);
        let wifi_profiles_key = hkcu.open_subkey_with_flags("Software\\Microsoft\\WLAN Profiles", enums::KEY_READ).unwrap();
        
        for (name, _) in wifi_profiles_key.enum_keys().unwrap() {
            println!("Profile Name: {}", name);
            
            // Retrieve password for each profile
            let profile_key = wifi_profiles_key.open_subkey_with_flags(&format!("{}\\Security\\SharedKey", name), enums::KEY_READ).unwrap();
            if let Some(password) = profile_key.get_value::<String>("SharedKeyData").ok() {
                println!("Password: {}", password);
            } else {
                println!("No password found for this profile.");
            }
        }
    }
    ```

### Step 3: Build and Run the Project
1. **Build the Project**:
   - In your terminal, run `cargo build` to compile the project.
2. **Run the Program**:
   - Execute the compiled program with `cargo run`.

### Step 4: Protect Your Credentials
- Ensure that any sensitive operations are performed in a secure environment.
- Use tools like Keeper Security for managing and securing passwords.

## Category
security