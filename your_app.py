import streamlit as st
import requests
from bs4 import BeautifulSoup
import random


def show_homepage():
    st.write("##i'm still working on cleaning the articles##")

def show_article_list(articles):
    st.title("Tyler's Stolen Articles")
    st.subheader("this site is for personal use to get an overview of the latest AI news")
    for index, article in enumerate(articles):
        if st.button(article['title'], key=f"article_{index}"):
            st.session_state['current_article_index'] = index
            st.session_state['view_article'] = True
            if 'viewed_articles' not in st.session_state:
                st.session_state['viewed_articles'] = []
            if article['title'] not in st.session_state['viewed_articles']:
                st.session_state['viewed_articles'].append(article['title'])

def fetch_article_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title').text if soup.find('title') else "Article Title Not Found"
    paragraphs = soup.find_all('p')
    content_html = ''.join(f'<p>{paragraph.text}</p>' for paragraph in paragraphs)
    return title, content_html

def fetch_articles():
    articles_list = []
    urls = [
        'https://www.technologyreview.com/topic/artificial-intelligence/',
        'https://news.mit.edu/topic/artificial-intelligence2'
    ]
    # Your scraping logic here
    # This is a placeholder for demonstration purposes
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        if 'technologyreview' in url:
            articles = soup.find_all('a', href=True)
            for article in articles:
                if "/2024/" in article['href']:
                    title = article.get_text(strip=True)
                    link = article['href']
                    articles_list.append({"title": title, "url": link})

        elif 'mit.edu' in url:
            articles = soup.find_all('article')
            for article in articles:
                title_element = article.find('h3')
                link_element = article.find('a', href=True)

                if title_element and link_element:
                    title = title_element.text.strip()
                    link = link_element['href'] if link_element['href'].startswith('http') else 'https://news.mit.edu/' + link_element['href']
                    articles_list.append({"title": title, "url": link})

    return articles_list




def show_article_content(articles):
    # List of image URLs
    image_urls = [
        "https://img.freepik.com/premium-vector/mountain-line-art-mid-century-modern-minimalist-art-print-abstract-contemporary-aesthetic-backgrounds-landscapes-vector-illustration_69626-538.jpg?w=2000",
        "https://img.freepik.com/premium-vector/mountain-ocean-wave-line-art-print-abstract-mountain-contemporary-aesthetic-backgrounds-landscapes-vector-illustrations_69626-739.jpg",
        "https://img.freepik.com/premium-vector/ocean-wave-landscape-creative-minimalist-modern-art-print-abstract-contemporary-aesthetic-backgrounds-landscapes-with-ocean-wave-sea-hill-skyline-vector-illustrations_69626-759.jpg",
        "https://img.freepik.com/premium-vector/creative-minimalist-modern-line-art-print-abstract-mountain-contemporary-aesthetic-backgrounds-landscapes-with-mountain-moon-sea-skyline-wave-vector-illustrations_69626-741.jpg"
    ]
    
    # Select a random image URL from the list
    random_image_url = random.choice(image_urls)
    
    current_index = st.session_state['current_article_index']
    article = articles[current_index]
    
    # Display the random image
    st.write("yo guys reload to access the list again.")

    st.image(random_image_url, caption="chosen aesthetic by tyler!", use_column_width=True)
    
    # Display the article content (assuming this functionality is already implemented)
    article_title, article_content_html = fetch_article_content(article['url'])
    st.markdown(f"## {article_title}", unsafe_allow_html=True)
    st.markdown(article_content_html, unsafe_allow_html=True)

    # Display the "Back" and "Next" buttons at the top
    col1, col2, col3 = st.columns([1,6,1])
    with col1:
        if st.button("Back"):
            st.session_state['view_article'] = False
    with col3:
        if current_index + 1 < len(articles):
            if st.button("Next", key="next_article"):
                next_index = current_index + 1
                next_article_title = articles[next_index]['title']
                if 'viewed_articles' not in st.session_state:
                    st.session_state['viewed_articles'] = [next_article_title]
                elif next_article_title not in st.session_state['viewed_articles']:
                    st.session_state['viewed_articles'].append(next_article_title)
                st.session_state['current_article_index'] = next_index



def show_history(articles):
    st.sidebar.title("Viewed Articles")
    for title in st.session_state.get('viewed_articles', []):
        if st.sidebar.button(title, key=f"history_{title}"):
            # Find the article by title to get its index
            for i, article in enumerate(articles):
                if article['title'] == title:
                    st.session_state['current_article_index'] = i
                    st.session_state['view_article'] = True
                    break

def main():
    show_homepage()
    articles = fetch_articles()
    show_history(articles)
    if 'view_article' in st.session_state and st.session_state['view_article']:
        show_article_content(articles)
    else:
        show_article_list(articles)

main()

        
