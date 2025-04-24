from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, HiddenField, SelectField, DecimalField
from wtforms.validators import DataRequired

class ProductoForma(FlaskForm):
    id = HiddenField('id')
    nombre = StringField('Nombre', validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired()])
    precio = DecimalField('Precio', places=2, validators=[DataRequired()])  # Cambiado a DecimalField
    categoria = SelectField('Categoria', choices=[], validators=[DataRequired()])
    guardar = SubmitField('Guardar')

    def cargar_categorias(self, categorias):
        """Carga dinámicamente las categorías en el campo SelectField."""
        # Las categorías ya son tuplas (id, nombre), así que no necesitas acceder a atributos
        self.categoria.choices = categorias
