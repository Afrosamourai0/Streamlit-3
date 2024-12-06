import streamlit as st
from streamlit_authenticator import Authenticate
import pandas as pd
from streamlit_option_menu import option_menu

# Charger les données des comptes utilisateurs à partir du fichier CSV
lesDonneesDesComptes = pd.read_csv('CSV_utilisateurs.csv')

# Initialisation du dictionnaire des données des comptes
comptes = {'usernames': {}}
for iter, row in lesDonneesDesComptes.iterrows():
    comptes['usernames'][row['name']] = {
        'name': row['name'],
        'password': row['password'],
        'email': row['email'],
        'role': row['role']
    }

# Initialisation de l'authentificateur
authenticator = Authenticate(
    comptes,  # Les données des comptes
    "cookie_name",  # Le nom du cookie, un str quelconque
    "cookie_key",  # La clé du cookie, un str quelconque
    30  # Le nombre de jours avant que le cookie expire
)

# Affichage du titre de la page
st.title("Bienvenue chez nous")

# Authentification de l'utilisateur
authenticator.login()

# Définition de la fonction d'accueil
def accueil():
    username = st.session_state['name']  # Récupère le nom de l'utilisateur connecté
    st.title(f"Bienvenue, {username} sur le contenu réservé aux utilisateurs connectés")
    st.image("https://as2.ftcdn.net/v2/jpg/01/76/66/53/1000_F_176665367_e7RvXL9vx86EmX7aPtMHHQfXtevNuLGP.jpg")
    st.write("""
    Voici une brève introduction et des informations sur ce que les utilisateurs connectés peuvent attendre. 
    Utilisez le menu latéral pour naviguer à travers les sections.
    """)

# Contrôle de l'état d'authentification
if st.session_state["authentication_status"]:
    # Création du menu dans la barre latérale avec des icônes
    with st.sidebar:
        selection = option_menu(
            menu_title="Menu",
            options=["Accueil", "Photos", "Déconnexion"],
            icons=["house", "image", "box-arrow-right"],
            menu_icon="cast",
            default_index=0,
        )

        # Ajout du selectbox et du radio button dans la sidebar
        contact_method = st.selectbox(
            "How would you like to be contacted?",
            ("Email", "Home phone", "Mobile phone")
        )
        shipping_method = st.radio(
            "Choose a shipping method",
            ("Standard (5-15 days)", "Express (2-5 days)")
        )

    if selection == "Accueil":
        accueil()
    elif selection == "Photos":
        st.subheader("Galerie de Photos")
        with st.expander("Voir les photos"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.image("https://posts-cdn.kueez.net/OAyTRw3lzuXbeail/image-NIyKOaLH4pIYVt57.jpg", caption="Crazy_Shot")
            with col2:
                st.image("https://posts-cdn.kueez.net/OAyTRw3lzuXbeail/image-88Zpwf5hlktP8YsV.jpg", caption="Crazy_Shot 2")
            with col3:
                st.image("https://posts-cdn.kueez.net/OAyTRw3lzuXbeail/image-z47R84eNnwcne1zK.jpg", caption="Crazy_Shot 3")
    elif selection == "Déconnexion":
        authenticator.logout("Déconnexion", "sidebar")

elif st.session_state["authentication_status"] is False:
    st.error("L'username ou le password est/sont incorrect")
elif st.session_state["authentication_status"] is None:
    st.warning('Les champs username et mot de passe doivent être remplis')
