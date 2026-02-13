import streamlit as st
import requests

# Config

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Movie-Recommendation-System",
    page_icon="🎬",
    layout="wide",
)

# Head

st.title("🎬 :red[Movie Recommender]")
st.markdown("Hybride Recommendation + TMDB Integeration")

st.divider()

# Sidebar

st.sidebar.header("User Input")

user_id = st.sidebar.number_input(
    "Enter User ID",
    min_value=1,
    step=1,
    placeholder="Type the ID..."
)

top_n = st.sidebar.number_input(
    "Number of Recommendation",
    min_value=3,
    max_value=20,
    value=10
) 

recommend_button = st.sidebar.button("Get Recommendation")


# main logic part

if recommend_button:

    with st.spinner("wait for it..", show_time=True):

        try:
            response = requests.get(
                f"{API_URL}/recommend/user/{user_id}",
                params={"top_n": top_n}
            )

            if response.status_code !=200:
                st.error("Error fetching recommendations")
                st.stop()

            data = response.json()
            recommendation = data["recommendations"]

            if not recommendation:
                st.warning("No recommendation found.")

            st.success(f"Top {top_n} Recommendation for User {user_id}")

            st.divider()

            # Display Movies in grid

            cols = st.columns(6)

            for idx, movie in enumerate(recommendation):

                with cols[idx % 6]:
                    if movie['poster_url']:
                        st.image(movie['poster_url'], width="stretch")

                    st.subheader(movie['title'])

                    if movie["rating"]:
                        st.write(f"⭐️ Rating: {movie['rating']}")

                    if movie["overview"]:
                        with st.expander("Overview"):
                            st.write(movie["overview"])

        except Exception as e:
            st.error(f"Something went wrong: {e}")

