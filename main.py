import concurrent
import os
from concurrent.futures import ThreadPoolExecutor

from saxonche import PySaxonProcessor
from saxonche import PySaxonApiError

def transform(saxon_processor, xslt30_executable, file_name):
    try:
        xdm_node = saxon_processor.parse_xml(xml_file_name=f'input/{file_name}')
        xslt30_executable.set_global_context_item(xdm_item=xdm_node)
        xslt30_executable.apply_templates_returning_file(xdm_value=xdm_node, output_file=f'output/{file_name}')
        return True
    except PySaxonApiError as e:
        return e.message
def thread_pool_test():
    with PySaxonProcessor() as saxon_processor:
        xslt30_compiler = saxon_processor.new_xslt30_processor()

        try:
            xslt30_executable = xslt30_compiler.compile_stylesheet(stylesheet_file='identity.xsl')
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = {executor.submit(transform, saxon_processor, xslt30_executable, file): file for file in os.listdir('input')}
                for future in concurrent.futures.as_completed(futures):
                    file = futures[future]
                    result = future.result()
                    if (result == True):
                        print(f'File {file} transformed successfully!')
                    else:
                        print(f'File {file} transformation failed with {result}')

        except PySaxonApiError as e:
            print(f'XSLT compilation failed: {e}')



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    thread_pool_test()

