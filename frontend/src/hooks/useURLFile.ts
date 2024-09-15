import { useEffect, useState } from "react";

export default function useURLFile( url: string, filename: string ){
    const [file, setFile] = useState<File | null>(null);
    const [pending, setPending] = useState<boolean>(true);
    const [error, setError] = useState<Error | null>(null);

    useEffect(() => {
        fetch(url)
          .then(res => res.blob())
          .then(blob => {
            setFile(new File([blob], filename, {type: 'image/jpeg'}));
            setPending(false);
          })
          .catch(err => {
            setPending(false);
            setError(err)
          })
    }, [url, filename])

    return [file as File, pending as boolean, error as Error]
}