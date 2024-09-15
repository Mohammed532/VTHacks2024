import { ChangeEventHandler, MouseEventHandler, useRef } from "react"

type FileDrawerProp = {
    title: string,
    files: string[],
    fileChangeFn?: ChangeEventHandler<HTMLInputElement>,
    addFileButton?: boolean,
    className?: string
}

export default function FileDrawer({ title, className, files, fileChangeFn }: FileDrawerProp){
    const fileInputRef = useRef<HTMLInputElement>(null);

    let openFile:MouseEventHandler<HTMLButtonElement> = (e) => {
        e.preventDefault();
        fileInputRef.current?.click() 
    }

    return(
        <div className={`${className}`}>
            <div className="flex flex-row justify-between items-center m-2">
                <h3 className="text-2xl font-medium">{title}</h3>
                <button className="btn btn-secondary p-1" onClick={openFile}>+</button>
                <input 
                 type="file" 
                 id={`${title}-file`} 
                 ref={fileInputRef} 
                 className="hidden" 
                 onChange={fileChangeFn}
                 multiple
                 accept="image/*"/>
            </div>
            <div className="bg-secondary rounded h-[40vh] overflow-x-scroll ">
                <div className="flex flex-row m-9 gap-3">
                    {files.map((img, idx) => (
                        <img key={idx} src={img} alt={`img-${idx}`} className="object-scale-down max-h-[30vh]" />
                    ))}
                </div>
            </div>
        </div>
    )
}