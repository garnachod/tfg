class SupportWeb(object):
	"""Proporciona funciones utiles para mejorar la interfaz web"""
	@staticmethod
	def addGeneralStructureMid(cadena=""):
		retorno = '''
					<div class="mid">
						<div class="mid-cont">
							<div class="cont-general">
				  '''

		retorno += cadena
		
		retorno += '''
					</div>
						</div>
							</div>
				   '''	  
		return retorno