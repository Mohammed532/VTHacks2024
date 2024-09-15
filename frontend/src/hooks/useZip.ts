import JSZip from "jszip"

export default function useZip(filename: string){
    const zip = new JSZip();

    let createZipFn = (files: FileList | File[]) => {
        Array.from(files).forEach(f => {
            zip.file(f.name, f)
        });

        zip.generateAsync({ type: "blob" })
          .then(content => {
            const link = document.createElement("a");
            link.href = URL.createObjectURL(content);
            link.download = `${filename}.zip`;
            link.click();
          })
    }

    return createZipFn;

}