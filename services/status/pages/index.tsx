import useSWR from "swr";
import ServiceCard from "../components/ServiceCard";

const fetcher = (url: string) => fetch(url).then((res) => res.json());

export default function Home() {
    const {data, error} = useSWR("/api/health", fetcher, {refreshInterval: 10000});

    if (error) return <p>Error cargando estado de los servicios.</p>;
    if (!data) return <p>Cargando...</p>;

    return (
        <div className="container mx-auto py-10">
            <h1 className="text-2xl font-bold text-center">Estado de los Servicios</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-5">
                {data.map((service) => (
                    <ServiceCard key={service.name} name={service.name} status={service.status}/>
                ))}
            </div>
        </div>
    );
}
