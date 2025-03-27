from sqlalchemy.orm import Session
from e_server.c_con.src.database.models.user_product.user_product_Interaction_model import UserProductInteraction
from src.schemas.user_product_Interaction_schema import UserProductInteractionCreate



class UserProductInteraction:
    def __init__(self, db: Session):
        self.db = db

    def create_user_product_interaction(self, user_product_interaction):
        """
        Create a new user_product_interaction in the database.

        Parameters:
            user_product_interaction (UserProductInteractionCreate): The user_product_interaction to be created.

        Returns:
            UserProductInteraction: The newly created user_product_interaction.
        """

        self.db.add(user_product_interaction)
        self.db.commit()
        self.db.refresh(user_product_interaction)
        return user_product_interaction

    def get_user_product_interaction(self, user_id, product_id):
        """
        Retrieve a specific user-product interaction from the database.

        Parameters:
            user_id (int): The ID of the user.
            product_id (int): The ID of the product.

        Returns:
            UserProductInteraction: The user-product interaction record, or None if not found.
        """

        return self.db.query(UserProductInteraction).filter_by(user_id=user_id, product_id=product_id).first()

    def update_user_product_interaction(self, user_product_interaction):
        """
        Update an existing user-product interaction in the database.

        Parameters:
            user_product_interaction (UserProductInteraction): The user-product interaction instance with updated values.

        Returns:
            UserProductInteraction: The updated user-product interaction.
        """

        self.db.merge(user_product_interaction)
        self.db.commit()
        return user_product_interaction
    
    def delete_user_product_interaction(self, user_product_interaction):
        """
        Delete an existing user-product interaction from the database.

        Parameters:
            user_product_interaction (UserProductInteraction): The user-product interaction instance to be deleted.

        Returns:
            UserProductInteraction: The deleted user-product interaction.
        """
        self.db.delete(user_product_interaction)
        self.db.commit()
        return user_product_interaction