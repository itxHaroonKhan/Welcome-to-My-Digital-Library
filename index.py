import streamlit as st
import json
from streamlit.components.v1 import html

def load_books():
    """Load books from a JSON file."""
    try:
        with open("books_data.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_books():
    """Save current book collection to JSON file."""
    with open("books_data.json", "w") as f:
        json.dump(st.session_state.books, f, indent=4)

st.set_page_config(page_title="Book Manager", page_icon="📚", layout="wide")

# Custom CSS with animations and better styling
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        .book-card {
            padding: 20px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin: 10px 0;
            transition: transform 0.2s;
        }
        .book-card:hover {
            transform: translateY(-2px);
        }
        .stButton>button {
            background: #007acc;
            color: white;
            border-radius: 8px;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            transform: scale(1.05);
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        .status-badge {
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.8em;
        }
        .read-true {background: #c8e6c9; color: #2e7d32;}
        .read-false {background: #ffecb3; color: #f57f17;}
    </style>
""", unsafe_allow_html=True)

st.title("📚 Book Collection Manager")
st.session_state.books = load_books()

# Rainbow divider animation
html("<marquee style='width: 100%; color: #007acc' scrollamount='10'>✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦</marquee>")

action = st.sidebar.radio(
    "📋 Menu",
    ["🏠 Home", "➕ Add Book", "🗑️ Delete Book", "✏️ Update Book", "🔍 Search Books", "📊 Reading Stats"],
    index=0
)

if action == "🏠 Home":
    st.header("🌟 Welcome to My Digital Library!")
    st.image("https://i.pinimg.com/originals/f9/62/45/f962450691e20c1fbcd502b4652c4e3d.gif", use_container_width=True)
    st.write("""
    ### 📖 Your Personal Book Haven
    Organize, track, and celebrate your reading journey!
    - Add new books with ➕ Add Book
    - Manage your collection with ✏️ Update and 🗑️ Delete
    - Track your progress with 📊 Reading Stats
    """)

elif action == "➕ Add Book":
    st.header("📘 Add New Book")
    with st.form("add_form", clear_on_submit=True):
        cols = st.columns(2)
        title = cols[0].text_input("📖 Title*")
        author = cols[1].text_input("✍️ Author*")
        year = cols[0].text_input("📅 Publication Year")
        genre = cols[1].text_input("🎭 Genre")
        read = st.checkbox("✅ Mark as read")

        if st.form_submit_button("🚀 Add Book"):
            if title and author:
                new_book = {
                    "title": title.strip(),
                    "author": author.strip(),
                    "year": year.strip(),
                    "genre": genre.strip(),
                    "read": read
                }
                st.session_state.books.append(new_book)
                save_books()
                st.success("🎉 Book added successfully!")
                st.balloons()
            else:
                st.error("❌ Please fill required fields (Title & Author)!")

elif action == "🗑️ Delete Book":
    st.header("❌ Remove Book from Collection")
    if st.session_state.books:
        book_titles = [f"{book['title']} by {book['author']}" for book in st.session_state.books]
        to_delete = st.selectbox("📚 Select book to delete:", book_titles)

        if st.button("🗑️ Confirm Delete"):
            index = book_titles.index(to_delete)
            del st.session_state.books[index]
            save_books()
            st.success("🔥 Book successfully deleted!")
            st.snow()
    else:
        st.warning("📭 Your library is empty!")

elif action == "✏️ Update Book":
    st.header("🖋️ Update Book Details")
    if st.session_state.books:
        book_titles = [f"{book['title']} by {book['author']}" for book in st.session_state.books]
        selected = st.selectbox("📚 Select book to update:", book_titles)
        index = book_titles.index(selected)
        book = st.session_state.books[index]

        with st.form("update_form"):
            new_title = st.text_input("📖 Title*", value=book['title'])
            new_author = st.text_input("✍️ Author*", value=book['author'])
            new_year = st.text_input("📅 Year", value=book['year'])
            new_genre = st.text_input("🎭 Genre", value=book['genre'])
            new_read = st.checkbox("✅ Read", value=book['read'])

            if st.form_submit_button("💾 Save Changes"):
                if new_title and new_author:
                    st.session_state.books[index] = {
                        "title": new_title.strip(),
                        "author": new_author.strip(),
                        "year": new_year.strip(),
                        "genre": new_genre.strip(),
                        "read": new_read
                    }
                    save_books()
                    st.success("📌 Book updated successfully!")
                else:
                    st.error("❌ Title and Author are required!")
    else:
        st.warning("📭 No books to update!")

elif action == "🔍 Search Books":
    st.header("🔎 Explore Your Library")
    search_term = st.text_input("", placeholder="🔍 Search by title, author, or genre...")
    results = [book for book in st.session_state.books
               if search_term.lower() in book['title'].lower()
               or search_term.lower() in book['author'].lower()
               or search_term.lower() in book['genre'].lower()]

    if search_term:
        st.subheader(f"📖 Found {len(results)} results:")
        for book in results:
            with st.container():
                st.markdown(f"""
                <div class="book-card">
                    <h4>📚 {book['title']}</h4>
                    <p>✍️ {book['author']}</p>
                    <div style="display: flex; gap: 10px; margin-top: 10px;">
                        <div class="status-badge {'read-true' if book['read'] else 'read-false'}">
                            {'✅ Read' if book['read'] else '📖 Reading'}
                        </div>
                        <div>📅 {book['year']}</div>
                        <div>🎭 {book['genre']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("🌟 Type something to start searching...")

elif action == "📊 Reading Stats":
    st.header("📈 Your Reading Journey")
    total = len(st.session_state.books)
    read = sum(book['read'] for book in st.session_state.books)
    progress = (read / total * 100) if total > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("📚 Total Books", total, "Library Size")
    col2.metric("✅ Books Read", read, f"{progress:.1f}% Completed")
    col3.metric("📖 To Read", total - read, "Remaining")

    st.progress(progress/100 if total > 0 else 0)

    if total > 0:
        st.subheader("📊 Genre Distribution")
        genres = [book['genre'] for book in st.session_state.books if book['genre']]
        if genres:
            genre_count = {g: genres.count(g) for g in set(genres)}
            st.bar_chart(genre_count)
        else:
            st.info("🎭 Add genres to see distribution!")
    else:
        st.warning("📭 Start adding books to see statistics!")

# Add some floating emojis using HTML
html("""
<div style="position: fixed; bottom: 20px; right: 20px; font-size: 30px;">
    <div style="animation: float 3s infinite;">📖</div>
    <div style="animation: float 3s infinite 0.5s;">✨</div>
    <div style="animation: float 3s infinite 1s;">🌟</div>
</div>

<style>
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
    100% { transform: translateY(0px); }
}
</style>
""")

st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📚 Library Tips
- Use **genre tags** like #fiction or #biography
- Mark books as read to track progress
- Update details as you get new information
- Search using any keyword in title/author/genre
""")
