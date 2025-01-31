import type {NextApiRequest, NextApiResponse} from "next";

const SERVICES = [
    {name: "Tracking Service", url: "http://tracking-service:8000/health/"},
    {name: "Kafka", url: "http://kafka:9092"},
    {name: "RabbitMQ", url: "http://rabbitmq:15672/api/healthchecks/node"},
    {name: "MongoDB", url: "http://mongo:27017"},
    {name: "Prometheus", url: "http://prometheus:9090/-/healthy"},
];

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
    const statuses = await Promise.all(
        SERVICES.map(async (service) => {
            try {
                const response = await fetch(service.url);
                return {name: service.name, status: response.ok ? "UP" : "DOWN"};
            } catch {
                return {name: service.name, status: "DOWN"};
            }
        })
    );

    res.status(200).json(statuses);
}
