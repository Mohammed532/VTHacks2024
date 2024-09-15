import { ChangeEventHandler, MouseEventHandler, useRef } from "react"

type FileDrawerProp = {
    title: string,
    files: string[],
    fileChangeFn?: ChangeEventHandler<HTMLInputElement>,
    addFileButton?: boolean,
    className?: string
}

export default function FileDrawer({ title, files, fileChangeFn, addFileButton, className }: FileDrawerProp){
    const fileInputRef = useRef<HTMLInputElement>(null);

    let openFile:MouseEventHandler<HTMLButtonElement> = (e) => {
        e.preventDefault();
        fileInputRef.current?.click() 
    }

    let deleteImg: MouseEventHandler<HTMLSpanElement> = (e) => {

    }

    return(
        <div className={`${className}`}>
            <div className="flex flex-row justify-between items-center m-2">
                <h3 className="text-2xl font-medium">{title}</h3>
                {addFileButton && 
                <button className="btn btn-secondary p-1" onClick={openFile}>+</button>
                }   
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
                <div className="flex flex-row items-center m-9 gap-7 w-max">
                    {files.map((img, idx) => (
                        <div key={idx} className="group indicator h-fit">
                            {false && <span id={`${idx}`} onClick={deleteImg} className={`indicator-item indicator-top indicator-end badge badge-primary invisible text-white group-hover:visible hover:cursor-pointer hover:brightness-90`}>x</span>}
                            <img src={img} alt={`img-${idx}`} className="object-scale-down max-h-[30vh]" />
                        </div>
                        ))}
                    </div>
                </div>
            </div>
        )
}