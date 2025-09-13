from PyPDF2 import PdfReader, PdfWriter
import os
import glob

class Divider:
    def __init__(self, path: str, name_file: str, base_output_name: str):
        self._path = path
        self._name_file = name_file
        self._base_out_name = base_output_name
        self._output_dir = "./output"
        self._text_dir = "./text"

    @staticmethod
    def list_output_pdfs(directory: str = "./output") -> list[str]:
        return glob.glob(os.path.join(directory, "*.pdf"))

    @classmethod
    def from_full_path(cls, full_path: str, base_output_name: str):
        path, name_file = os.path.split(full_path)
        return cls(path, name_file, base_output_name)

    def _create_directory(self, directory: str) -> None:
        os.makedirs(directory, exist_ok=True)

    def _get_pdf_reader(self) -> PdfReader | None:
        file_path = os.path.join(self._path, self._name_file)
        print(f"Abriendo PDF: {file_path}")
        try:
            return PdfReader(file_path)
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo PDF en {file_path}")
            return None

    def _generate_pdf_output_filename(self, page_number: int) -> str:
        return os.path.join(
            self._output_dir,
            f'{self._base_out_name}_pagina_{page_number}.pdf'
        )

    def _save_page_as_pdf(self, page, page_number: int) -> None:
        pdf_writer = PdfWriter()
        pdf_writer.add_page(page)
        output_filename = self._generate_pdf_output_filename(page_number)
        with open(output_filename, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)
        print(f'Creado: {output_filename}')

    def split_pdf(self) -> None:
        self._create_directory(self._output_dir)
        pdf = self._get_pdf_reader()
        if not pdf:
            return

        print(f"El PDF tiene {len(pdf.pages)} páginas. Dividiendo...")
        for i, page in enumerate(pdf.pages):
            self._save_page_as_pdf(page, i + 1)

    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        reader = PdfReader(pdf_path)
        text_content = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text_content += extracted + "\n"
        return text_content.strip()

    def _generate_txt_output_filename(self, pdf_path: str) -> str:
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        return os.path.join(self._text_dir, f"{base_name}.txt")

    def _save_text_to_file(self, text: str, pdf_path: str) -> None:
        txt_filename = self._generate_txt_output_filename(pdf_path)
        with open(txt_filename, "w", encoding="utf-8") as txt_file:
            txt_file.write(text)
        print(f"Texto extraído en: {txt_filename}")

    def _process_pdf_for_text_extraction(self, pdf_file: str) -> None:
        text_content = self._extract_text_from_pdf(pdf_file)
        self._save_text_to_file(text_content, pdf_file)

    def pdfs_to_text(self) -> None:
        self._create_directory(self._text_dir)
        pdf_files = self.list_output_pdfs(self._output_dir)
        if not pdf_files:
            print(f"No se encontraron archivos PDF en '{self._output_dir}'.")
            return

        print(f"\nConvirtiendo {len(pdf_files)} archivos PDF a texto...")
        for pdf_file in pdf_files:
            self._process_pdf_for_text_extraction(pdf_file)

if __name__ == "__main__":
    print("Ejecutando ejemplo de Divider...")
    pdf_input_path = os.path.join("data", "LaNocheBocaArriba.pdf")
    if os.path.exists(pdf_input_path):
        divider = Divider.from_full_path(pdf_input_path, "LaNocheBocaArriba")
        divider.split_pdf()
        divider.pdfs_to_text()
        print("\nEjemplo de Divider finalizado.")
    else:
        print(f"Archivo de prueba no encontrado en '{pdf_input_path}'")
        print("Por favor, añade un PDF a la carpeta 'data' para ejecutar el ejemplo.")
