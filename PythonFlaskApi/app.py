from flask import Flask, request
from flask_restful import Api, Resource
from dotenv import load_dotenv
import os
import pymysql
import numpy as np

load_dotenv()

app = Flask(__name__)
api = Api(app)


class RecommendationResource(Resource):
    @staticmethod
    def get(self):
        product_id = request.args.get('product_id')  # Input product ID for which you want recommendations

        # Connect to the database
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            db=os.getenv('DB_NAME'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                # Retrieve the product's features
                cursor.execute("""
                    SELECT categories.category_name AS category, colors.color AS color, products_attr.attribute1, products_attr.attribute2, ...
                    FROM products
                    JOIN categories ON products.category_id = categories.id
                    JOIN products_attr ON products_attr.products_id = products.id
                    JOIN colors ON products_attr.color_id = colors.id
                    WHERE products.id = %s
                """, (product_id,))
                product = cursor.fetchone()

                # Compute similarity based on features
                cursor.execute("""
                    SELECT products.id, products.name, products_attr.attribute1, products_attr.attribute2, ...
                    FROM products
                    JOIN categories ON products.category_id = categories.id
                    JOIN products_attr ON products_attr.products_id = products.id
                    JOIN colors ON products_attr.color_id = colors.id
                    WHERE categories.category_name = %s AND colors.color = %s AND products.id != %s
                """, (product['category'], product['color'], product_id))
                recommendations = cursor.fetchall()

                # Calculate similarity scores
                similarity_scores = []
                for recommendation in recommendations:
                    similarity_score = RecommendationResource.calculate_similarity(product, recommendation)
                    similarity_scores.append((recommendation, similarity_score))

                # Sort recommendations by similarity score in descending order
                sorted_recommendations = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

                # Return top recommended products
                top_recommendations = [rec[0] for rec in sorted_recommendations[:5]]

        finally:
            connection.close()

        return top_recommendations

    @staticmethod
    def calculate_similarity(product1, product2):
        # Compute similarity between product1 and product2 based on their attributes
        # You can use any similarity metric like cosine similarity, Euclidean distance, etc.
        # Here's an example using cosine similarity
        attributes1 = [product1['attribute1'], product1['attribute2'], ...]
        attributes2 = [product2['attribute1'], product2['attribute2'], ...]
        similarity = np.dot(attributes1, attributes2) / (np.linalg.norm(attributes1) * np.linalg.norm(attributes2))
        return similarity


api.add_resource(RecommendationResource, '/recommendations')

if __name__ == '__main__':
    app.run(debug=True)
