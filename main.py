from app.presentation.cli.main_menu import MainMenu

def main():
    # Initialisation du menu principal
    app = MainMenu()
    try:
        app.afficher_accueil()
    except KeyboardInterrupt:
        print("\nApplication fermée.")

if __name__ == "__main__":
    main()