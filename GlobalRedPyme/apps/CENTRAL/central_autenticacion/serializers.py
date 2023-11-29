from rest_framework import serializers

from apps.CENTRAL.central_usuarios.models import Usuarios


# class RegistrationSerializer(serializers.ModelSerializer):

# 	password2 				= serializers.CharField(style={'input_type': 'password'}, write_only=True)

# 	class Meta:
# 		model = Usuarios
# 		fields = ['email', 'username', 'password', 'password2','idRol']
# 		extra_kwargs = {
# 				'password': {'write_only': True},
# 		}	


# 	def	save(self):

# 		usuario= Usuarios(
# 					email=self.validated_data['email'],
# 					username=self.validated_data['username'],
# 					idRol=self.validated_data['idRol']
# 				)
# 		password = self.validated_data['password']
# 		password2 = self.validated_data['password2']
# 		if password != password2:
# 			raise serializers.ValidationError({'password': 'Passwords must match.'})
# 		usuario.set_password(password)
# 		usuario.save()
# 		return usuario


