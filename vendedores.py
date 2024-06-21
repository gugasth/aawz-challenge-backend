class Vendedores:
    """
    Classe Vendedores para gerenciar vendedores com operações CRUD.

    Atributos da Classe:
    -------------------
    vendedores (list): Lista de todos os vendedores.
    id_counter (int): Contador para gerar IDs únicos para os vendedores.

    Atributos da Instância:
    ----------------------
    id (int): ID único do vendedor.
    nome (str): Nome do vendedor.
    cpf (str): CPF do vendedor.
    data_nascimento (str): Data de nascimento do vendedor.
    email (str): Email do vendedor.
    estado (str): Estado (UF) do vendedor.
    """

    vendedores = []
    id_counter = 1

    def __init__(self, nome, cpf, data_nascimento, email, estado):
        """
        Inicializa uma nova instância da classe Vendedores.

        Args:
        -----
        nome (str): Nome do vendedor.
        cpf (str): CPF do vendedor.
        data_nascimento (str): Data de nascimento do vendedor.
        email (str): Email do vendedor.
        estado (str): Estado (UF) do vendedor.
        """
        self.id = Vendedores.id_counter
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.email = email
        self.estado = estado
        Vendedores.id_counter += 1
        Vendedores.vendedores.append(self)

    @classmethod
    def criar(cls, nome, cpf, data_nascimento, email, estado):
        """
        Cria um novo vendedor e o adiciona à lista de vendedores.

        Args:
        -----
        nome (str): Nome do vendedor.
        cpf (str): CPF do vendedor.
        data_nascimento (str): Data de nascimento do vendedor.
        email (str): Email do vendedor.
        estado (str): Estado (UF) do vendedor.

        Returns:
        --------
        Vendedores: A nova instância do vendedor criada.
        """
        return cls(nome, cpf, data_nascimento, email, estado)

    @classmethod
    def ler(cls, vendedor_id=None):
        """
        Lê um ou todos os vendedores da lista de vendedores.

        Args:
        -----
        vendedor_id (int, optional): ID do vendedor a ser lido. Se None, lê todos os vendedores.

        Returns:
        --------
        Vendedores ou list: O vendedor correspondente ao ID ou a lista de todos os vendedores.
        """
        if vendedor_id:
            return next((vendedor for vendedor in cls.vendedores if vendedor.id == vendedor_id), None)
        return cls.vendedores

    @classmethod
    def atualizar(cls, vendedor_id, nome=None, cpf=None, data_nascimento=None, email=None, estado=None):
        """
        Atualiza os dados de um vendedor existente.

        Args:
        -----
        vendedor_id (int): ID do vendedor a ser atualizado.
        nome (str, optional): Novo nome do vendedor.
        cpf (str, optional): Novo CPF do vendedor.
        data_nascimento (str, optional): Nova data de nascimento do vendedor.
        email (str, optional): Novo email do vendedor.
        estado (str, optional): Novo estado (UF) do vendedor.

        Returns:
        --------
        Vendedores: O vendedor atualizado.
        """
        vendedor = cls.ler(vendedor_id)
        if vendedor:
            vendedor.nome = nome if nome else vendedor.nome
            vendedor.cpf = cpf if cpf else vendedor.cpf
            vendedor.data_nascimento = data_nascimento if data_nascimento else vendedor.data_nascimento
            vendedor.email = email if email else vendedor.email
            vendedor.estado = estado if estado else vendedor.estado
        return vendedor

    @classmethod
    def deletar(cls, vendedor_id):
        """
        Deleta um vendedor da lista de vendedores.

        Args:
        -----
        vendedor_id (int): ID do vendedor a ser deletado.

        Returns:
        --------
        Vendedores: O vendedor deletado.
        """
        vendedor = cls.ler(vendedor_id)
        if vendedor:
            cls.vendedores.remove(vendedor)
        return vendedor
