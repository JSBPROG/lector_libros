from PyPDF2 import PdfReader, PdfWriter
import os
import glob


class Divider:
    """
    Divide un archivo PDF en páginas y extrae su contenido de texto.

    Esta clase toma un archivo PDF, lo divide en múltiples archivos PDF de
    una sola página y luego extrae el contenido de texto de cada una de
    esas páginas, guardándolo en archivos .txt.

    Parameters
    ----------
    path : str
        Ruta al directorio donde se encuentra el archivo PDF de entrada.
    name_file : str
        Nombre del archivo PDF que se va a dividir.
    base_output_name : str
        Nombre base para los archivos de salida (PDFs y TXTs).

    Attributes
    ----------
    __path : str
        Ruta privada al directorio del archivo PDF.
    __name_file : str
        Nombre privado del archivo PDF original.
    __base_out_name : str
        Nombre base privado para los archivos de salida.
    """

    def __init__(self, path: str, name_file: str, base_output_name: str):
        """
        Inicializa la clase Divider.

        Parameters
        ----------
        path : str
            Ruta al directorio donde se encuentra el archivo PDF de entrada.
        name_file : str
            Nombre del archivo PDF que se va a dividir.
        base_output_name : str
            Nombre base para los archivos de salida.
        """
        self.__path = path
        self.__name_file = name_file
        self.__base_out_name = base_output_name

    @staticmethod
    def list_output_pdfs(directory: str = "./output") -> list[str]:
        """
        Lista los archivos PDF dentro de un directorio específico.

        Parameters
        ----------
        directory : str, optional
            Ruta del directorio donde se buscarán los archivos PDF.
            Por defecto es './output'.

        Returns
        -------
        list[str]
            Una lista de rutas a los archivos PDF encontrados.
        """
        return glob.glob(os.path.join(directory, "*.pdf"))

    @classmethod
    def from_full_path(cls, full_path: str, base_output_name: str):
        """
        Crea una instancia de Divider a partir de una ruta completa al archivo.

        Parameters
        ----------
        full_path : str
            Ruta completa al archivo PDF (incluyendo nombre y extensión).
        base_output_name : str
            Nombre base para los archivos resultantes.

        Returns
        -------
        Divider
            Una nueva instancia de la clase Divider.
        """
        path, name_file = os.path.split(full_path)
        return cls(path, name_file, base_output_name)

    def split_pdf(self) -> None:
        """
        Divide el archivo PDF de entrada en páginas individuales.

        Cada página se guarda como un archivo PDF independiente en la carpeta
        './output'. El nombre de cada archivo se forma con el
        `base_output_name` y el número de página.
        """
        output_dir = "./output"
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(self.__path, self.__name_file)
        
        print(f"Abriendo PDF: {file_path}")
        try:
            pdf = PdfReader(file_path)
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo PDF en {file_path}")
            return

        print(f"El PDF tiene {len(pdf.pages)} páginas. Dividiendo...")
        for i, page in enumerate(pdf.pages):
            pdf_writer = PdfWriter()
            pdf_writer.add_page(page)

            output_filename = os.path.join(
                output_dir,
                f'{self.__base_out_name}_pagina_{i + 1}.pdf'
            )
            with open(output_filename, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)
            print(f'Creado: {output_filename}')

    def pdfs_to_text(self, output_dir: str = "./output", text_dir: str = "./text") -> None:
        """
        Convierte los archivos PDF de un directorio a archivos de texto.

        Busca todos los archivos PDF en `output_dir`, extrae su contenido
        de texto y lo guarda en archivos .txt dentro de `text_dir`.

        Parameters
        ----------
        output_dir : str, optional
            Directorio que contiene los archivos PDF por página.
            Por defecto es './output'.
        text_dir : str, optional
            Directorio donde se guardarán los archivos de texto resultantes.
            Por defecto es './text'.
        """
        os.makedirs(text_dir, exist_ok=True)

        pdf_files = self.list_output_pdfs(output_dir)
        if not pdf_files:
            print(f"No se encontraron archivos PDF en '{output_dir}'.")
            return

        print(f"\nConvirtiendo {len(pdf_files)} archivos PDF a texto...")
        for pdf_file in pdf_files:
            reader = PdfReader(pdf_file)
            text_content = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text_content += extracted + "\n"

            base_name = os.path.splitext(os.path.basename(pdf_file))[0]
            txt_filename = os.path.join(text_dir, f"{base_name}.txt")

            with open(txt_filename, "w", encoding="utf-8") as txt_file:
                txt_file.write(text_content.strip())

            print(f"Texto extraído en: {txt_filename}")


if __name__ == "__main__":
    # Ejemplo de uso
    print("Ejecutando ejemplo de Divider...")
    # En la carpeta data debe haber un archivo
    # Por ejemplo: ./data/prueba.pdf
    pdf_input_path = os.path.join("data", "LaNocheBocaArriba.pdf")
    if os.path.exists(pdf_input_path):
        divider = Divider.from_full_path(pdf_input_path, "LaNocheBocaArriba")
        divider.split_pdf()
        divider.pdfs_to_text()
        print("\nEjemplo de Divider finalizado.")
    else:
        print(f"Archivo de prueba no encontrado en '{pdf_input_path}'")
        print("Por favor, añade un PDF a la carpeta 'data' para ejecutar el ejemplo.")