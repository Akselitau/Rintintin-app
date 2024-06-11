import React from 'react';
import './ReservationCard.css';

interface ReservationCardProps {
    reservation: {
        reservation_id: number;
        dog_id: number;
        pension_id: number;
        start_date: string;
        end_date: string;
        status: string;
        pension_name: string;
        dog_name: string;
        dog_breed: string;
    };
}

const ReservationCard: React.FC<ReservationCardProps> = ({ reservation }) => {
    return (
        <div className="reservation-card">
            <h2>{reservation.pension_name}</h2>
            <p>Date de début: {reservation.start_date}</p>
            <p>Date de fin: {reservation.end_date}</p>
            <p>Chien: {reservation.dog_name} ({reservation.dog_breed})</p>
            <p>Status: {reservation.status}</p>
        </div>
    );
};

export default ReservationCard;
