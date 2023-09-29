def search_posts_by_name(query, posts):
    results = []

    for post in posts:
        post_name = post[3]
        if query.lower() in post_name.lower():
            results.append(post)

    return results
